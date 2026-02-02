window.shareConfession = function (cardId) {
    const element = document.getElementById(cardId);
    if (!element) return;

    // Clone to remove buttons for the screenshot
    const clone = element.cloneNode(true);
    clone.style.position = 'fixed'; // Use fixed to ensure it stays in viewport context for rendering
    clone.style.left = '-9999px';
    clone.style.top = '0';
    clone.style.width = element.offsetWidth + 'px'; // Enforce width
    clone.style.height = 'auto'; // Allow growing
    clone.style.maxHeight = 'none';
    clone.style.transform = 'none'; // Remove rotation for clean screenshot

    // Find text container and expand it
    const textContainer = clone.querySelector('.cust-scroll');
    if (textContainer) {
        textContainer.style.maxHeight = 'none';
        textContainer.style.overflow = 'visible';
    }

    // Remove action buttons from clone?
    // User wants them to appear in the screenshot
    // const actions = clone.querySelector('.card-actions');
    // if (actions) actions.remove();

    // Add branding watermark
    const waterMark = document.createElement('div');
    waterMark.innerText = 'sifess.app';
    waterMark.className = 'absolute bottom-2 right-4 text-xs font-bold opacity-50 text-black';
    clone.appendChild(waterMark);

    document.body.appendChild(clone);

    html2canvas(clone, {
        backgroundColor: null,
        scale: 2, // High res
        useCORS: true, // Handle external fonts/images
        allowTaint: true, // Allow tainting the canvas with cross-origin content
        logging: false
    }).then(canvas => {
        document.body.removeChild(clone);

        canvas.toBlob(blob => {
            const file = new File([blob], 'confession.png', { type: 'image/png' });

            if (navigator.share) {
                navigator.share({
                    title: 'Check this out on SIFESS!',
                    text: 'Someone sent me this!',
                    files: [file]
                }).catch(err => console.log('Share failed', err));
            } else {
                const link = document.createElement('a');
                link.download = 'sifess-confession.png';
                link.href = canvas.toDataURL();
                link.click();
            }
        });
    });
}
