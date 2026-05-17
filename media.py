import os
import sys
import subprocess
import time
from pathlib import Path

REQUIRED_MODULES = {
	"rich": "rich",
	"inquirer": "inquirer",
	"yt_dlp": "yt-dlp"
}

def check_and_install_modules():
	missing_modules = []
	for module_name, pip_name in REQUIRED_MODULES.items():
		try:
			__import__(module_name)
		except ImportError:
			missing_modules.append(pip_name)
	if missing_modules:
		print("[!] Mendeteksi module yang belum terinstall...")
		print(f"[!] Menyiapkan instalasi otomatis untuk: {', '.join(missing_modules)}")
		print("[!] Mohon tunggu, sedang memproses pip install...\n")
		time.sleep(1.5)
		try:
			subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_modules])
			print("\n[+] Semua module berhasil diinstall otomatis!")
			print("[+] Membuka tools...\n")
			time.sleep(1.5)
		except subprocess.CalledProcessError:
			print("\n[-] Gagal menginstall module secara otomatis.")
			print("[-] Pastikan koneksi internet aktif dan jalankan 'pkg upgrade -y' di Termux.")
			sys.exit(1)

check_and_install_modules()

import inquirer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn

console = Console()
DEFAULT_DOWNLOAD_DIR = Path("/sdcard/Download")

def clear_screen():
	os.system("clear" if os.name != "nt" else "cls")

def draw_banner():
	banner_text = (
		"[magenta]╦ ╦╔╦╗ ╔╦╗╦  ╔═╗[/magenta]\n"
		"[magenta]╚╦╝ ║───║║║  ╠═╝[/magenta]  [bold cyan]Build Version[/bold cyan]\n"
		"[magenta] ╩  ╩  ═╩╝╩═╝╩  [/magenta]  [white]3.1.0 (Multi-Platform)[/white]\n"
		"                  [bold reverse magenta] KEYBOARDWARRIOR | OFFICIAL [/bold reverse magenta]\n\n"
		"[bold cyan]Social Media Downloader[/bold cyan]\n"
		"[dim white]Support: YouTube, Facebook, & Instagram[/dim white]"
	)
	console.print(Panel(banner_text, border_style="magenta", expand=False))

def get_save_path(subfolder: str) -> Path:
	console.print(f"\n[bold yellow]ℹ️ Info:[/bold yellow] Format path default internal: [cyan]/sdcard/Download/[/cyan]")
	user_input = input(f"➔ Masukkan lokasi simpan (Enter jika ingin di {DEFAULT_DOWNLOAD_DIR / subfolder}): ").strip()
	if not user_input:
		target_path = DEFAULT_DOWNLOAD_DIR / subfolder
	else:
		target_path = Path(user_input)
	try:
		target_path.mkdir(parents=True, exist_ok=True)
	except PermissionError:
		console.print("[bold red]❌ Gagal:[/bold red] Izin akses penyimpanan ditolak! Jalankan 'termux-setup-storage'.")
		sys.exit(1)
	return target_path

def hook_ytdlp_progress(d, progress_bar, task_id):
	if d['status'] == 'downloading':
		total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
		downloaded = d.get('downloaded_bytes', 0)
		progress_bar.update(task_id, total=total, completed=downloaded)
	elif d['status'] == 'finished':
		progress_bar.update(task_id, description="[bold green]🔄 Muxing & Finishing File...[/bold green]")

def eksekusi_download(url_list: list, subfolder: str, butuh_login=False):
	folder_tujuan = get_save_path(subfolder)
	for index, url in enumerate(url_list, start=1):
		clear_screen()
		draw_banner()
		console.print(Panel(f"[bold cyan]Mengunduh Antrean ke-{index} dari {len(url_list)}[/bold cyan]\n[dim white]Target: {url}[/dim white]", border_style="cyan"))
		output_template = str(folder_tujuan / "%(title)s_%(id)s.%(ext)s")
		progress_bar = Progress(
			TextColumn("[bold blue]{task.description}"),
			BarColumn(bar_width=25, complete_style="green", finished_style="bright_green"),
			DownloadColumn(),
			TransferSpeedColumn(),
			TimeRemainingColumn(),
			console=console
		)
		with progress_bar:
			task_id = progress_bar.add_task(f"[bold yellow]📥 Downloader [/bold yellow]", total=None)
			import yt_dlp
			ydl_opts = {
				'format': 'bestvideo+bestaudio/best',
				'merge_output_format': 'mp4',
				'outtmpl': output_template,
				'progress_hooks': [lambda d: hook_ytdlp_progress(d, progress_bar, task_id)],
				'quiet': True,
				'no_warnings': True,
				'ignoreerrors': True
			}
			if butuh_login:
				ydl_opts['cookiesfrombrowser'] = ('chrome',) 
			try:
				with yt_dlp.YoutubeDL(ydl_opts) as ydl:
					ydl.download([url])
				console.print(f"[bold green]✔ Sukses mengunduh antrean ke-{index}![/bold green]\n")
			except Exception as e:
				console.print(f"[bold red]❌ Gagal pada antrean ke-{index}:[/bold red] {e}\n")
		time.sleep(1.5)
	console.print(f"[bold green]✔ PROSES SELESAI![/bold green] File disimpan di: [underline cyan]{folder_tujuan}[/underline cyan]")
	input("\nTekan Enter untuk kembali...")

def parse_multi_urls(raw_text: str) -> list:
	normalized = raw_text.replace(",", " ").replace("\n", " ")
	return [u.strip() for u in normalized.split(" ") if u.strip()]

def dapatkan_input_url():
	console.print("\n[bold yellow]➔ Masukkan URL target (Bisa Multi-Link)[/bold yellow]")
	console.print("[dim white]Pisahkan dengan koma, spasi, atau Enter. Tekan Enter 2x jika sudah selesai:[/dim white]")
	lines = []
	while True:
		try:
			line = input()
			if not line and not lines:
				break
			if not line:
				break
			lines.append(line)
		except KeyboardInterrupt:
			break
	raw_url_input = " ".join(lines)
	return parse_multi_urls(raw_url_input)

def sub_menu_youtube():
	while True:
		clear_screen()
		draw_banner()
		questions = [
			inquirer.List('opsi', message="Menu YouTube", choices=[
				('1. Download Video (Reguler/Multi)', '1'),
				('2. Download Shorts (Vertikal/Multi)', '2'),
				('3. Bulk Download Channel/Playlist Video', '3'),
				('4. Bulk Download Channel/Playlist Shorts', '4'),
				('➔ Kembali ke Menu Utama', 'kembali')
			], carousel=True)
		]
		ans = inquirer.prompt(questions)
		if not ans or ans['opsi'] == 'kembali': break
		urls = dapatkan_input_url()
		if not urls: continue
		mapping = {'1': 'YT_Videos', '2': 'YT_Shorts', '3': 'YT_Bulk_Videos', '4': 'YT_Bulk_Shorts'}
		eksekusi_download(urls, mapping[ans['opsi']])

def sub_menu_facebook():
	while True:
		clear_screen()
		draw_banner()
		questions = [
			inquirer.List('opsi', message="Menu Facebook", choices=[
				('1. Download FB Reels', '1'),
				('2. Download FB Story (Harus Publik / Login)', '2'),
				('3. Download FB Video Reguler', '3'),
				('➔ Kembali ke Menu Utama', 'kembali')
			], carousel=True)
		]
		ans = inquirer.prompt(questions)
		if not ans or ans['opsi'] == 'kembali': break
		urls = dapatkan_input_url()
		if not urls: continue
		mapping = {'1': 'FB_Reels', '2': 'FB_Stories', '3': 'FB_Videos'}
		butuh_login = True if ans['opsi'] == '2' else False
		eksekusi_download(urls, mapping[ans['opsi']], butuh_login=butuh_login)

def sub_menu_instagram():
	while True:
		clear_screen()
		draw_banner()
		questions = [
			inquirer.List('opsi', message="Menu Instagram", choices=[
				('1. Download IG Reels', '1'),
				('2. Download IG Story (Memerlukan Akses/Cookies)', '2'),
				('➔ Kembali ke Menu Utama', 'kembali')
			], carousel=True)
		]
		ans = inquirer.prompt(questions)
		if not ans or ans['opsi'] == 'kembali': break
		urls = dapatkan_input_url()
		if not urls: continue
		mapping = {'1': 'IG_Reels', '2': 'IG_Stories'}
		butuh_login = True if ans['opsi'] == '2' else False
		eksekusi_download(urls, mapping[ans['opsi']], butuh_login=butuh_login)

def main_menu():
	while True:
		clear_screen()
		draw_banner()
		questions = [
			inquirer.List(
				'platform',
				message="Pilih Platform Sosial Media",
				choices=[
					('YouTube Downloader Menu', 'yt'),
					('Facebook Downloader Menu', 'fb'),
					('Instagram Downloader Menu', 'ig'),
					('Keluar Aplikasi', 'keluar')
				],
				carousel=True
			)
		]
		answers = inquirer.prompt(questions)
		if not answers or answers['platform'] == 'keluar':
			console.print("\n[bold yellow]Keluar dari aplikasi. Sampai jumpa lagi bor! 👋[/bold yellow]")
			break
		platform = answers['platform']
		if platform == 'yt':
			sub_menu_youtube()
		elif platform == 'fb':
			sub_menu_facebook()
		elif platform == 'ig':
			sub_menu_instagram()

if __name__ == "__main__":
	try:
		main_menu()
	except KeyboardInterrupt:
		console.print("\n\n[bold red]Program dihentikan paksa (Ctrl+C).[/bold red]")
		sys.exit(0)
