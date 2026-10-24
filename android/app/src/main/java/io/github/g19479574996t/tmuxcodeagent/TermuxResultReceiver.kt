package io.github.g19479574996t.tmuxcodeagent

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Bundle

class TermuxResultReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action != ACTION_RESULT) return
        val outer = intent.extras
        val result = outer?.getBundle(EXTRA_RESULT_BUNDLE)
            ?: outer?.keySet()
                ?.asSequence()
                ?.mapNotNull { key -> outer.getBundle(key) }
                ?.firstOrNull()
        val text = formatResult(result, outer)
        ResultStore.lastResult = text
        ResultStore.listener?.invoke(text)
    }

    private fun formatResult(result: Bundle?, outer: Bundle?): String {
        if (result == null) return "Termux returned a result, but no structured result bundle was found."
        fun firstString(vararg names: String): String =
            names.firstNotNullOfOrNull { name ->
                result.getString(name)
            }?.trim().orEmpty()

        fun firstInt(vararg names: String): Int? =
            names.firstNotNullOfOrNull { name ->
                if (result.containsKey(name)) {
                    result.getInt(name)
                } else {
                    null
                }
            }

        val exit = firstInt(
            "exitCode",
            "exit_code",
            "com.termux.RUN_COMMAND_RESULT_EXIT_CODE",
        )

        val stdout = firstString(
            "stdout",
            "com.termux.RUN_COMMAND_RESULT_STDOUT",
        )

        val stderr = firstString(
            "stderr",
            "com.termux.RUN_COMMAND_RESULT_STDERR",
        )

        val errmsg = firstString(
            "errmsg",
            "errorMessage",
            "com.termux.RUN_COMMAND_RESULT_ERRMSG",
        )
        val lines = mutableListOf<String>()
        lines += if (exit?.toString() == "0") "Launch: SUCCESS" else "Launch result received"
        if (exit != null) lines += "Exit code: $exit"
        if (stdout.isNotEmpty()) lines += "stdout:\n$stdout"
        if (stderr.isNotEmpty()) lines += "stderr:\n$stderr"
        if (errmsg.isNotEmpty()) lines += "error:\n$errmsg"
        if (lines.size == 1) lines += "Result keys: ${result.keySet().sorted().joinToString()}"
        return lines.joinToString("\n")
    }

    companion object {
        const val ACTION_RESULT = "io.github.g19479574996t.tmuxcodeagent.RESULT"
        const val EXTRA_RESULT_BUNDLE = "com.termux.RUN_COMMAND_RESULT"
    }
}

object ResultStore {
    var lastResult: String = "Ready"
    var listener: ((String) -> Unit)? = null
}
