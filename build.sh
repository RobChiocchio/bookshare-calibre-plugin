#/bin/bash
flatpak run --command=calibre-debug com.calibre_ebook.calibre -e ./build_ui.py $(flatpak document-export -trw calibre-plugin/ -a com.calibre_ebook.calibre)