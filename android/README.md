# tmux-code-agent Android companion

Application ID: `io.github.g19479574996t.tmuxcodeagent`

The APK is a companion launcher. Termux remains the runtime.

Prerequisites:
1. Termux installed.
2. `com.termux.permission.RUN_COMMAND` granted to this app.
3. `allow-external-apps=true` in `~/.termux/termux.properties` and Termux restarted.
4. tmux-code-agent installed at the path in `TermuxContract.kt`.

Build requirements for the pinned AGP 9.0.1 configuration: JDK 17, Gradle 9.1.0, Android SDK / Build Tools 36.0.0.
