import flet as ft

from download import download, fetch_appid, fetch_contentid


def parse_urls(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def load_urls_from_file(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as handle:
        return [line.strip() for line in handle.read().splitlines() if line.strip()]


def main(page: ft.Page) -> None:
    page.title = "Steam Workshop Downloader"
    page.window_width = 920
    page.window_height = 720
    page.padding = 20

    urls_field = ft.TextField(
        label="Workshop URLs (one per line)",
        multiline=True,
        min_lines=8,
        max_lines=12,
        expand=True,
    )

    log_view = ft.ListView(expand=True, spacing=6, auto_scroll=True)

    def log(message: str) -> None:
        log_view.controls.append(ft.Text(message))
        page.update()

    def set_running(is_running: bool) -> None:
        download_button.disabled = is_running
        load_button.disabled = is_running
        file_path_field.disabled = is_running
        clear_button.disabled = is_running
        page.update()

    def merge_urls(new_urls: list[str]) -> None:
        if not new_urls:
            log("No URLs found in file.")
            return
        existing = parse_urls(urls_field.value)
        existing_set = set(existing)
        merged = existing + [url for url in new_urls if url not in existing_set]
        urls_field.value = "\n".join(merged)
        log(f"Added {len(merged) - len(existing)} URL(s) from file.")
        page.update()

    def on_load_file(event: ft.ControlEvent) -> None:
        path = file_path_field.value.strip()
        if not path:
            log("Enter a file path first.")
            return
        try:
            merge_urls(load_urls_from_file(path))
        except Exception as exc:
            log(f"Failed to read file: {exc}")

    def on_clear(event: ft.ControlEvent) -> None:
        urls_field.value = ""
        log_view.controls.clear()
        page.update()

    def download_worker(urls: list[str]) -> None:
        try:
            pairs: list[tuple[int, int]] = []
            for url in urls:
                log(f"Resolving: {url}")
                contentid = fetch_contentid(url)
                appid = fetch_appid(contentid)
                pairs.append((appid, contentid))
            log(f"Starting download for {len(pairs)} item(s)...")
            download(pairs)
            log("Done.")
        except Exception as exc:
            log(f"Error: {exc}")
        finally:
            set_running(False)

    def on_download(event: ft.ControlEvent) -> None:
        urls = parse_urls(urls_field.value)
        if not urls:
            log("No URLs to download.")
            return
        set_running(True)
        page.run_thread(lambda: download_worker(urls))

    file_path_field = ft.TextField(
        label="URLs file path (.txt)",
        hint_text="C:\\path\\urls.txt",
        expand=True,
    )
    download_button = ft.Button("Download", on_click=on_download)
    load_button = ft.Button("Load file", on_click=on_load_file)
    clear_button = ft.Button("Clear", on_click=on_clear)

    page.add(
        ft.Column(
            [
                ft.Text("Steam Workshop Downloader", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("SteamCMD must be installed and available in PATH."),
                urls_field,
                ft.Row([file_path_field, load_button], spacing=10),
                ft.Row([download_button, clear_button], spacing=10),
                ft.Text("Log", size=16, weight=ft.FontWeight.W_600),
                log_view,
            ],
            expand=True,
            spacing=12,
        )
    )


if __name__ == "__main__":
    ft.run(main)
