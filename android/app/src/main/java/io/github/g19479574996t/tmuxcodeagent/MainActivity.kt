package io.github.g19479574996t.tmuxcodeagent

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.Settings
import android.view.Gravity
import android.view.ViewGroup
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import android.app.Activity

class MainActivity : Activity() {
    private lateinit var status: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val pad = (20 * resources.displayMetrics.density).toInt()
        status = TextView(this).apply { text = ResultStore.lastResult; textSize = 16f }
        val launch = Button(this).apply {
            text = "Launch in Termux"
            setOnClickListener {
                if (!TermuxLauncher.termuxInstalled(this@MainActivity)) {
                    status.text = "Termux is not installed or not visible."
                } else try {
                    TermuxLauncher.launch(this@MainActivity)
                    status.text = "Launch request sent to Termux."
                } catch (e: SecurityException) {
                    status.text = "Grant Run commands in Termux environment permission and enable allow-external-apps=true."
                } catch (e: Exception) {
                    status.text = "Launch failed: ${e.message}"
                }
            }
        }
        val settings = Button(this).apply {
            text = "Open app settings"
            setOnClickListener {
                startActivity(Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:$packageName")))
            }
        }
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(pad, pad, pad, pad)
            addView(TextView(this@MainActivity).apply { text = "tmux-code-agent\nRC2 Android companion"; textSize = 26f }, ViewGroup.LayoutParams(-1, -2))
            addView(TextView(this@MainActivity).apply { text = "Termux remains the runtime. This app only requests launch through RunCommandService."; textSize = 15f }, ViewGroup.LayoutParams(-1, -2))
            addView(status, ViewGroup.LayoutParams(-1, -2))
            addView(launch, ViewGroup.LayoutParams(-1, -2))
            addView(settings, ViewGroup.LayoutParams(-1, -2))
        }
        setContentView(root)
    }

    override fun onStart() {
        super.onStart()
        ResultStore.listener = { runOnUiThread { status.text = it } }
    }

    override fun onStop() {
        ResultStore.listener = null
        super.onStop()
    }
}
