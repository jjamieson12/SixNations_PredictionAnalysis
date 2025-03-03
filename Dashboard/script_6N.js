document.querySelectorAll('.click-to-enlarge').forEach(img => {
    img.addEventListener('click', function() {
        const modal = document.getElementById('imageModal');
        const modalImg = document.getElementById('modalImg');
        const modalContent = document.querySelector('.modal-content');
        document.getElementById('modalImg').src = this.src;
        modal.style.display = 'flex'; // Show modal when image is clicked
        // Adjust max width for small screens
        if (window.innerWidth < 1200) {  // Adjust breakpoint as needed
            modalContent.style.maxWidth = '100%'; // Full width on small screens
            modalImg.style.width = '100%'; // Scale to fit
        } else {
            modalContent.style.maxWidth = '50%'; // Default for larger screens
            modalImg.style.width = 'auto'; // Keep natural width
        }
    });
});

document.querySelector('.close').addEventListener('click', function() {
    document.getElementById('imageModal').style.display = 'none'; // Hide modal when close is clicked
});
