# بناء ملف السطب (Aura Setup)

ملف سطب ويندوز شكله مودرن، بيثبّت اللانشر، وبينزّل أيقونة على سطح المكتب تلقائي،
ومعاه Uninstaller.

## مرة واحدة: ثبّت الأدوات

```powershell
pip install pyinstaller pillow
winget install JRSoftware.InnoSetup      # أو من https://jrsoftware.org/isdl.php
```

## البناء

```powershell
.\build_installer.ps1 -Version 2.0.0
```

الناتج: **`installer\Output\Aura-Setup-2.0.0.exe`** — ده اللي بتوزّعه.

خطوات السكربت:
1. `installer\make_assets.py` → يولّد `app.ico` + `wizard.bmp` + `wizard-small.bmp` + `version_info.txt` من `logo.png`.
2. `pyinstaller Aura.spec` → يبني `dist\Aura.exe` (ملف واحد، بدون console).
3. `iscc installer\aura.iss` → يلفّه في ملف السطب.

خيارات:
- `-SkipBuild` — يستخدم `dist\Aura.exe` الموجود من غير ما يعيد بناء (أسرع وقت التجارب).
- `-Version x.y.z` — رقم النسخة (بيظهر في السطب، وفي Add/Remove Programs، وفي خصائص الـ exe).

## اللي المستخدم بيشوفه

- ويزارد بستايل `modern` + لوحة جانبية فيها اللوجو و "AURA".
- **تثبيت لكل مستخدم بدون UAC** (مفيش طلب صلاحيات أدمن). لو حب يثبّت لكل المستخدمين، الخيار متاح في أول شاشة.
- شاشة اختيار المجلد + **checkbox "أيقونة على سطح المكتب"** (متعلّمة افتراضيًا).
- في الآخر: **checkbox "افتح Aura"**.
- يقفل أي نسخة شغّالة قبل التحديث ويرجّع يفتحها.
- Start Menu group + Uninstaller. عند الحذف بيسأل لو عايز يمسح بياناتك (`%APPDATA%\MCLauncherPro`) — الافتراضي "لأ".

## التحديث التلقائي

بعد ما توزّع النسخة الأولى، النسخ الجاية بتتحدّث عند المستخدم لوحدها عبر GitHub Releases.
الخطوات كاملة في **`installer/UPDATES.md`** — باختصار: عدّل `__version__` في `core/version.py`،
ابنِ، واعمل GitHub release بـ tag `v<النسخة>` ومعاه ملف الـ Setup.

## ملاحظات

- الأصول المولّدة (`app.ico`, `*.bmp`, `version_info.txt`) ممكن ما تتحفظش في Git — بتتولّد كل build.
- رقم النسخة مصدره الوحيد `core/version.py` — `build_installer.ps1` بيقراه لو ما مرّرتش `-Version`.
- لو عايز بداية أسرع للانشر، حوّل `Aura.spec` من onefile لـ onedir (وعدّل `[Files]` في `aura.iss` لـ `dist\Aura\*` مع `recursesubdirs`).
- التوقيع الرقمي (code signing) مش مضمّن — من غيره SmartScreen ممكن يطلع تحذير أول مرة.
