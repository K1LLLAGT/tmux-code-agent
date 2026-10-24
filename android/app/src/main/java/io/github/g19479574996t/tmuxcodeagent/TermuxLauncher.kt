package io.github.g19479574996t.tmuxcodeagent

import android.app.PendingIntent
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build

object TermuxLauncher {
    fun termuxInstalled(context: Context): Boolean = try {
        context.packageManager.getPackageInfo(TermuxContract.TERMUX_PACKAGE, PackageManager.PackageInfoFlags.of(0))
        true
    } catch (_: Exception) { false }

    fun launch(context: Context) {
        val resultIntent = Intent(context, TermuxResultReceiver::class.java).apply {
            action = TermuxResultReceiver.ACTION_RESULT
        }
        val flags = PendingIntent.FLAG_ONE_SHOT or PendingIntent.FLAG_UPDATE_CURRENT or
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) PendingIntent.FLAG_MUTABLE else 0
        val pending = PendingIntent.getBroadcast(context, 10002, resultIntent, flags)

        val intent = Intent().apply {
            component = ComponentName(TermuxContract.TERMUX_PACKAGE, TermuxContract.RUN_COMMAND_SERVICE)
            action = TermuxContract.ACTION_RUN_COMMAND
            putExtra(TermuxContract.EXTRA_COMMAND_PATH, TermuxContract.LAUNCHER)
            putExtra(TermuxContract.EXTRA_ARGUMENTS, arrayOf("start"))
            putExtra(TermuxContract.EXTRA_WORKDIR, TermuxContract.WORKDIR)
            putExtra(TermuxContract.EXTRA_BACKGROUND, true)
            putExtra(TermuxContract.EXTRA_PENDING_INTENT, pending)
            putExtra(TermuxContract.EXTRA_COMMAND_LABEL, "tmux-code-agent")
            putExtra(TermuxContract.EXTRA_COMMAND_DESCRIPTION, "Launch tmux-code-agent RC2 companion session")
        }
        context.startService(intent)
    }
}
