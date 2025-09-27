document.addEventListener('DOMContentLoaded', function() {
    const burger = document.getElementById('burger-menu');
    const sidebarContainer = document.getElementById('sidebar-container');
    const sidebar = document.getElementById('sidebar');
    const burgerIcon = document.getElementById('burger-icon');
    const closeIcon = document.getElementById('close-icon');
    let sidebarOpen = false;

    function openSidebar() {
        sidebarContainer.classList.add('open');
        sidebar.classList.add('open');
        burgerIcon.style.display = 'none';
        closeIcon.style.display = 'block';
        sidebarOpen = true;
    }
    function closeSidebar() {
        sidebarContainer.classList.remove('open');
        sidebar.classList.remove('open');
        burgerIcon.style.display = 'block';
        closeIcon.style.display = 'none';
        sidebarOpen = false;
    }
    burger.onclick = function() {
        if (!sidebarOpen) {
            openSidebar();
        } else {
            closeSidebar();
        }
    };
    function handleResize() {
        if(window.innerWidth < 900) {
            burger.style.display = 'block';
            closeSidebar();
        } else {
            burger.style.display = 'none';
            sidebarContainer.classList.remove('open');
            sidebar.classList.remove('open');
            sidebarContainer.style.display = 'block';
            sidebarContainer.style.position = 'static';
            sidebarContainer.style.width = 'auto';
            sidebarContainer.style.height = 'auto';
            sidebarContainer.style.background = 'none';
            sidebar.style.position = 'static';
            sidebar.style.transform = 'none';
            sidebar.style.width = '220px';
            sidebar.style.height = 'auto';
            burgerIcon.style.display = 'block';
            closeIcon.style.display = 'none';
            sidebarOpen = false;
        }
    }
    window.addEventListener('resize', handleResize);
    handleResize();
});
