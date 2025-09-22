const express = require("express");
const { exec } = require("child_process");
const os = require("os");
const router = express.Router();

/**
 * Returns Raspberry Pi system diagnostics in structured format.
 * Example: GET /raspberry
 */

function runCommand(cmd) {
  return new Promise((resolve, reject) => {
    exec(cmd, (err, stdout) => {
      if (err) reject(err);
      else resolve(stdout);
    });
  });
}

router.get("/", async (req, res) => {
  const snapshot = {
    temperature_celsius: null,
    cpu_info: [],
    model_info: {},
    memory_info: {},
    os_info: {},
    errors: []
  };

  try {
    const [tempOut, cpuOut, memOut, unameOut] = await Promise.all([
      runCommand("vcgencmd measure_temp"),
      runCommand("cat /proc/cpuinfo"),
      runCommand("free -h"),
      runCommand("uname -a")
    ]);

    // 🌡️ Temperature
    const match = tempOut.match(/temp=([\d.]+)'C/);
    snapshot.temperature_celsius = match ? parseFloat(match[1]) : null;

    // 🧠 CPU Info
    const lines = cpuOut.split("\n");
    let currentCore = {};
    lines.forEach(line => {
      if (line.trim() === "") return;
      const [key, value] = line.split(":").map(s => s.trim());
      if (key === "processor") {
        if (Object.keys(currentCore).length > 0) snapshot.cpu_info.push(currentCore);
        currentCore = { processor: value };
      } else if (key === "Model") {
        snapshot.model_info.model = value;
      } else if (key === "Serial") {
        snapshot.model_info.serial = value;
      } else if (key === "Revision") {
        snapshot.model_info.revision = value;
      } else {
        currentCore[key] = value;
      }
    });
    if (Object.keys(currentCore).length > 0) snapshot.cpu_info.push(currentCore);

    // 🧮 Memory Info
    const memLines = memOut.trim().split("\n");
    const memValues = memLines[1].split(/\s+/);
    const swapValues = memLines[2].split(/\s+/);
    snapshot.memory_info = {
      total: memValues[1],
      used: memValues[2],
      free: memValues[3],
      shared: memValues[4],
      buff_cache: memValues[5],
      available: memValues[6],
      swap_total: swapValues[1],
      swap_used: swapValues[2],
      swap_free: swapValues[3]
    };

    // 🖥️ OS Info
    snapshot.os_info = {
      hostname: os.hostname(),
      platform: os.platform(),
      arch: os.arch(),
      release: os.release(),
      kernel: unameOut.trim()
    };

    res.status(200).json(snapshot);
  } catch (err) {
    snapshot.errors.push({ source: "system", message: err.message });
    res.status(500).json(snapshot);
  }
});

module.exports = router;
