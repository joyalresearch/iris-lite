import matplotlib.pyplot as plt


def plot_ndvi_change(change, output_path=None):
    """Plot spatial NDVI change."""

    change_array = change["change"]

    fig, ax = plt.subplots(figsize=(8, 7))

    image = ax.imshow(
        change_array,
        cmap="RdYlGn",
        vmin=-0.6,
        vmax=0.6,
    )

    colorbar = fig.colorbar(image, ax=ax)
    colorbar.set_label("ΔNDVI (After - Before)")

    ax.set_title("NDVI Change: 2021 to 2024")
    ax.set_xlabel("Pixel column")
    ax.set_ylabel("Pixel row")

    fig.tight_layout()

    if output_path is not None:
        fig.savefig(
            output_path,
            dpi=200,
            bbox_inches="tight",
        )

    return fig, ax