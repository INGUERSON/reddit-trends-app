import flet as ft
from execution.fetch_reddit_posts import get_reddit_instance, analyze_subreddit, analyze_subreddit_fallback
import threading
import time

def main(page: ft.Page):
    # --- Configuration & Theme ---
    page.title = "Reddit Trends"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 400
    page.window_height = 800
    page.bgcolor = "#111111"  # Deep dark background

    # Custom Colors
    PRIMARY = "#BB86FC"
    SURFACE = "#1E1E1E"
    BACKGROUND = "#121212"
    ERROR = "#CF6679"

    # --- State ---
    current_posts = []

    # --- UI Components ---

    def create_post_card(post, index):
        """Creates a sophisticated card for a single post."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text(str(index), weight=ft.FontWeight.BOLD, color=PRIMARY),
                                padding=5,
                                border=ft.border.all(1, PRIMARY),
                                border_radius=5,
                            ),
                            ft.Text(f"Score: {post['score']} | {post['num_comments']} Comments", size=12, color=ft.Colors.WHITE54),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Text(post['title'], weight=ft.FontWeight.W_600, size=16, color=ft.Colors.WHITE),
                    ft.Divider(color=ft.Colors.WHITE10, height=10),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Read Post",
                                url=post['url'],
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.BLUE_GREY_900,
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                height=30,
                            ),
                            ft.Text(f"Engagement: {post['engagement']}", size=11, color=ft.Colors.GREEN_400, italic=True)
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ],
                spacing=10
            ),
            padding=15,
            border_radius=15,
            bgcolor=SURFACE,
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
            on_hover=lambda e: highlight_card(e),
            margin=ft.Margin(bottom=10, left=0, right=0, top=0)
        )

    def highlight_card(e):
        e.control.bgcolor = "#2C2C2C" if e.data == "true" else SURFACE
        e.control.update()

    # --- Layout Containers ---
    
    header = ft.Container(
        content=ft.Column([
            ft.Text("Trending Now", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Text("Insights from r/n8n & r/automation", size=12, color=ft.Colors.WHITE54),
        ]),
        padding=ft.Padding(left=20, right=20, top=40, bottom=20),
        bgcolor=ft.Colors.TRANSPARENT, # Gradient effect simulation
    )

    posts_list = ft.ListView(
        expand=True,
        spacing=0,
        padding=20,
    )

    progress_ring = ft.ProgressRing(color=PRIMARY, visible=False)
    status_text = ft.Text("Ready to scan...", color=ft.Colors.WHITE54, size=12, text_align=ft.TextAlign.CENTER)

    # --- Logic ---

    def load_data(e):
        scan_button.disabled = True
        progress_ring.visible = True
        status_text.value = "Fetching data from Reddit..."
        posts_list.controls.clear()
        page.update()

        def fetch_process():
            try:
                reddit = get_reddit_instance()

                all_posts = []
                subreddits = ['n8n', 'automation']
                
                for sub in subreddits:
                    update_status_thread(f"Scanning r/{sub}...")
                    if reddit:
                        sub_posts = analyze_subreddit(reddit, sub, limit=50, top_count=5)
                    else:
                        sub_posts = analyze_subreddit_fallback(sub, limit=50, top_count=5)
                    all_posts.extend(sub_posts)
                
                # Sort combined posts just in case, though we want them grouped or top overall
                all_posts.sort(key=lambda x: x['engagement'], reverse=True)
                
                # Update UI
                count = 1
                for post in all_posts:
                    posts_list.controls.append(create_post_card(post, count))
                    count += 1
                    time.sleep(0.1) # Staggered effect
                    page.update()
                
                update_status_thread("Scan complete.")

            except Exception as ex:
                update_status_thread(f"Error: {str(ex)}", is_error=True)
            finally:
                scan_button.disabled = False
                progress_ring.visible = False
                page.update()

        threading.Thread(target=fetch_process, daemon=True).start()

    def update_status(message, is_error=False):
        status_text.value = message
        status_text.color = ERROR if is_error else ft.Colors.WHITE54
        progress_ring.visible = False
        scan_button.disabled = False
        page.update()

    # Thread-safe status update
    def update_status_thread(message, is_error=False):
        status_text.value = message
        status_text.color = ERROR if is_error else ft.Colors.WHITE54
        page.update()

    scan_button = ft.FloatingActionButton(
        icon=ft.Icons.REFRESH,
        bgcolor=PRIMARY,
        content=ft.Row([ft.Icon(ft.Icons.REFRESH, color=ft.Colors.BLACK), ft.Text("SCAN", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
        width=120,
        on_click=load_data
    )

    # --- Assembly ---
    page.add(
        ft.Column(
            [
                header,
                ft.Container(
                    content=ft.Column(
                        [status_text, progress_ring],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=10
                ),
                posts_list,
            ],
            expand=True
        )
    )
    page.floating_action_button = scan_button
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_FLOAT

if __name__ == "__main__":
    ft.app(main)
