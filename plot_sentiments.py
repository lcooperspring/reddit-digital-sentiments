import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

sns.set(style="whitegrid")
sns.set_context("notebook", font_scale=0.9)

def show_plot_window():
    try:
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')
    except AttributeError:
        try:
            mng.full_screen_toggle()
        except:
            pass
    plt.show()

def plot_sentiment_analysis(posts_df, comments_df):
    num_posts = len(posts_df)
    num_comments = len(comments_df)

    if num_posts == 0 or num_comments == 0:
        print("Warning: No posts or comments found for analysis.")
        return

    print(f"Posts DataFrame contains {num_posts} posts.")
    print(f"Comments DataFrame contains {num_comments} comments.")

    fig, axs = plt.subplots(2, 2, figsize=(16, 10))
    axs = axs.flatten()

    sns.histplot(posts_df['sentiment_score'], kde=True, color='blue', bins=10, ax=axs[0])
    axs[0].set_title(f'Sentiment Distribution in Posts (Total Posts: {num_posts})', fontsize=11)
    axs[0].set_xlabel('Sentiment Score', fontsize=10)
    axs[0].set_ylabel('Frequency', fontsize=10)
    post_mean = posts_df['sentiment_score'].mean()
    post_std = posts_df['sentiment_score'].std()
    post_min = posts_df['sentiment_score'].min()
    post_max = posts_df['sentiment_score'].max()
    axs[0].text(0.72, 0.05, f'Mean: {post_mean:.2f}\nSD: {post_std:.2f}\nMin: {post_min:.2f}\nMax: {post_max:.2f}',
                transform=axs[0].transAxes, fontsize=9,
                bbox=dict(facecolor='white', alpha=0.6, edgecolor='black', boxstyle='round,pad=0.4'))

    sns.boxplot(x=comments_df['sentiment_score'], color='green', ax=axs[1])
    axs[1].set_title(f'Sentiment Distribution in Comments (Total Comments: {num_comments})', fontsize=11)
    axs[1].set_xlabel('Sentiment Score', fontsize=10)
    comment_mean = comments_df['sentiment_score'].mean()
    comment_std = comments_df['sentiment_score'].std()
    comment_min = comments_df['sentiment_score'].min()
    comment_max = comments_df['sentiment_score'].max()
    axs[1].text(0.72, 0.05, f'Mean: {comment_mean:.2f}\nSD: {comment_std:.2f}\nMin: {comment_min:.2f}\nMax: {comment_max:.2f}',
                transform=axs[1].transAxes, fontsize=9,
                bbox=dict(facecolor='white', alpha=0.6, edgecolor='black', boxstyle='round,pad=0.4'))

    post_avg = None
    if not posts_df.empty:
        post_avg = posts_df.groupby("subreddit")["sentiment_score"].mean().reset_index()
        sns.barplot(data=post_avg, x="subreddit", y="sentiment_score", palette="coolwarm", ax=axs[2])
        axs[2].set_title("Average Sentiment of Posts by Subreddit", fontsize=11)
        axs[2].set_ylabel("Sentiment Score", fontsize=10)
        axs[2].set_xlabel("Subreddit", fontsize=10)
        axs[2].set_ylim(-1, 1)

    comment_avg = None
    if not comments_df.empty:
        comment_avg = comments_df.groupby("subreddit")["sentiment_score"].mean().reset_index()
        sns.barplot(data=comment_avg, x="subreddit", y="sentiment_score", palette="viridis", ax=axs[3])
        axs[3].set_title("Average Sentiment of Comments by Subreddit", fontsize=11)
        axs[3].set_ylabel("Sentiment Score", fontsize=10)
        axs[3].set_xlabel("Subreddit", fontsize=10)
        axs[3].set_ylim(-1, 1)

    plt.tight_layout()

    root = tk.Tk()
    root.withdraw()
    root.after(1, show_plot_window)
    root.mainloop()

    summary_lines = []
    summary_lines.append("===== Sentiment Analysis Summary =====\n")
    summary_lines.append(f"Total Posts: {num_posts}")
    summary_lines.append(f"Mean (Posts): {post_mean:.3f}, Std Dev: {post_std:.3f}, Min: {post_min:.3f}, Max: {post_max:.3f}\n")

    if post_avg is not None:
        summary_lines.append("Average Post Sentiment by Subreddit:")
        summary_lines.append(post_avg.to_string(index=False))
        summary_lines.append("")

    summary_lines.append(f"Total Comments: {num_comments}")
    summary_lines.append(f"Mean (Comments): {comment_mean:.3f}, Std Dev: {comment_std:.3f}, Min: {comment_min:.3f}, Max: {comment_max:.3f}\n")

    if comment_avg is not None:
        summary_lines.append("Average Comment Sentiment by Subreddit:")
        summary_lines.append(comment_avg.to_string(index=False))

    summary_lines.append("\n=======================================")

    print("\n".join(summary_lines))
