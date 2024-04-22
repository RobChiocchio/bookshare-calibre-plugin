#/bin/bash
flatpak run --command=calibre-debug com.calibre_ebook.calibre -s

flatpak ps | grep com.calibre_ebook.calibre | grep -oP "(^\\S+)" | while read -r pid; do
    flatpak kill $pid
done

flatpak run --command=calibre-customize com.calibre_ebook.calibre -b "calibre-plugin"
flatpak run --command=calibre-debug com.calibre_ebook.calibre -g $@
