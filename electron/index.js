const { app, BrowserWindow, ipcMain, shell } = require('electron');

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    win.loadFile('index.html');
}

app.whenReady().then(() => {
    createWindow();
});

ipcMain.on('open-file-in-obsidian', (event, filename) => {
    const rawVaultName = "phasewalk1-master";
    const obsidianVaultName = encodeURIComponent(rawVaultName);

    // filepath will look something like
    // '/home/<username>/Documents/<vault-name>/path/to/file.md'
    // We want to split this into 2 parts
    //   1. all the way up to <vault-name>
    //   2. the rest of the path

    const vaultNameIndex = filename.indexOf(rawVaultName);
    const vaultNameLength = rawVaultName.length;
    const filePath = filename.slice(vaultNameIndex + vaultNameLength + 1);
    const encodedFilePath = encodeURIComponent(filePath);

    const openCmd = `xdg-open obsidian://open?vault=${obsidianVaultName}&file=${encodedFilePath}`;
    console.log('Open URL:', openCmd);

    const { exec } = require('child_process');
    exec(openCmd, (err, stdout, stderr) => {
        if (err) {
            console.error('Error opening file:', err);
            return;
        }
        console.log('stdout:', stdout);
        console.error('stderr:', stderr);
    });

});