# Auto-update (GitHub Releases)

Aura checks GitHub for a newer release on startup, and offers a one-click update
that downloads the new installer, runs it silently, and reopens the launcher.

## One-time setup

1. Create a public GitHub repo for releases, e.g. `yourname/aura`.
2. Put the repo in **`core/version.py`**:
   ```python
   __version__ = "2.0.0"
   UPDATE_REPO = "yourname/aura"
   ```
   (A user can also override this in Settings -> "GitHub update repo".)
3. Build once and ship `installer\Output\Aura-Setup-2.0.0.exe` to your users.

## Publishing a new version

1. Bump `__version__` in `core/version.py` (e.g. `2.1.0`).
2. `.\build_installer.ps1`  (it reads the version from that file).
3. On GitHub: **Releases -> Draft a new release**
   - Tag: `v2.1.0`  (the leading `v` is optional; must be a real, non-prerelease, non-draft release)
   - Attach `installer\Output\Aura-Setup-2.1.0.exe` as an asset
   - Publish
4. Done. Every client with 2.0.x sees the prompt on its next launch.

## How the client behaves

- Startup (3s after the window opens) -> background check of
  `api.github.com/repos/<repo>/releases/latest`.
- If the release tag parses to a higher version than `__version__`, a dialog shows
  the release notes with **Update now / Later / Skip this version**.
- **Update now**: downloads the `.exe` asset to `%TEMP%\Aura-Update-Setup.exe`,
  then a detached helper runs `Aura-Setup /SILENT` and relaunches `Aura.exe`.
- **Skip this version**: remembers the version and won't prompt again for it
  (Settings -> uncheck/recheck, or a newer version, resets this).
- Auto-check can be turned off in Settings. A manual "Check for updates" button is
  always there.
- Auto-update only runs in the **installed build** (frozen exe on Windows); from
  source it just shows the notes.

## Notes

- The GitHub API allows 60 unauthenticated requests/hour per IP - plenty for a
  once-per-launch check.
- Exactly one `.exe` asset per release is expected. If you attach more, the first
  one listed is used.
- No code signing yet, so the silent installer still triggers SmartScreen the
  first few downloads until reputation builds. Signing the exe removes that.
