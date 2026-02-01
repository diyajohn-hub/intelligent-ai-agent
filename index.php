<?php
// Mock error data - in a real app, you'd fetch this from a log file or database
$logs = [
    ["type" => "CRITICAL", "msg" => "Memory leak detected in Worker-7", "time" => "14:02:01"],
    ["type" => "WARNING", "msg" => "Disk usage reaching 85%", "time" => "14:05:33"],
    ["type" => "ERROR", "msg" => "API Timeout: Connection refused (Port 80)", "time" => "14:10:12"],
    ["type" => "INFO", "msg" => "System heartbeat: OK", "time" => "14:12:00"],
];

function getSeverityColor($type) {
    return match($type) {
        'CRITICAL' => '#ff4d4d',
        'ERROR'    => '#ff944d',
        'WARNING'  => '#ffdb4d',
        default    => '#4dff88',
    };
}
?>

<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: #121212; font-family: 'Courier New', monospace; padding: 20px; color: #00ff41; }
        .terminal { background: #000; border: 1px solid #333; padding: 15px; border-radius: 5px; box-shadow: 0 0 20px rgba(0,0,0,0.5); }
        .line { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #222; }
        .msg { flex-grow: 1; margin-left: 10px; }
        .severity { font-weight: bold; padding: 2px 8px; border-radius: 3px; color: #000; font-size: 12px; min-width: 80px; text-align: center; }
        .time { color: #888; }
    </style>
</head>
<body>

<h3>_SYSTEM_ERROR_LOG_V1.0</h3>
<div class="terminal">
    <?php foreach ($logs as $log): ?>
    <div class="line">
        <span class="time">[<?php echo $log['time']; ?>]</span>
        <span class="msg"><?php echo $log['msg']; ?></span>
        <span class="severity" style="background: <?php echo getSeverityColor($log['type']); ?>">
            <?php echo $log['type']; ?>
        </span>
    </div>
    <?php endforeach; ?>
</div>

</body>
</html>