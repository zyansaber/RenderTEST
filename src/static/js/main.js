// 导航菜单控制
document.addEventListener('DOMContentLoaded', function() {
    // 侧边栏折叠/展开功能
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('sidebar-collapsed');
            mainContent.classList.toggle('main-content-expanded');
        });
    }
    
    // 移动端侧边栏显示/隐藏
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('sidebar-show');
        });
    }
    
    // 点击主内容区域时关闭移动端侧边栏
    mainContent.addEventListener('click', function() {
        if (window.innerWidth < 992 && sidebar.classList.contains('sidebar-show')) {
            sidebar.classList.remove('sidebar-show');
        }
    });
    
    // 高亮当前活动的导航项
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        }
    });
});

// 警告消息自动消失
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        setTimeout(function() {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 500);
        }, 5000);
    });
});

// 表单验证
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
});

// PowerBI报表嵌入
function embedPowerBIReport(embedUrl, containerId) {
    const container = document.getElementById(containerId);
    if (!container || !embedUrl) return;
    
    const iframe = document.createElement('iframe');
    iframe.className = 'powerbi-embed';
    iframe.src = embedUrl;
    iframe.setAttribute('allowFullScreen', true);
    
    container.innerHTML = '';
    container.appendChild(iframe);
}

// 确认删除对话框
function confirmDelete(event, message) {
    if (!confirm(message || '确定要删除吗？此操作不可撤销。')) {
        event.preventDefault();
    }
}

// 表格排序功能
document.addEventListener('DOMContentLoaded', function() {
    const tables = document.querySelectorAll('.sortable');
    
    tables.forEach(table => {
        const headers = table.querySelectorAll('th[data-sort]');
        
        headers.forEach(header => {
            header.addEventListener('click', function() {
                const column = this.dataset.sort;
                const order = this.dataset.order === 'asc' ? 'desc' : 'asc';
                
                // 重置所有表头的排序状态
                headers.forEach(h => {
                    h.dataset.order = '';
                    h.classList.remove('sort-asc', 'sort-desc');
                });
                
                // 设置当前表头的排序状态
                this.dataset.order = order;
                this.classList.add(order === 'asc' ? 'sort-asc' : 'sort-desc');
                
                // 排序表格行
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));
                
                rows.sort((a, b) => {
                    const aValue = a.querySelector(`td[data-column="${column}"]`).textContent;
                    const bValue = b.querySelector(`td[data-column="${column}"]`).textContent;
                    
                    if (order === 'asc') {
                        return aValue.localeCompare(bValue);
                    } else {
                        return bValue.localeCompare(aValue);
                    }
                });
                
                // 重新添加排序后的行
                rows.forEach(row => tbody.appendChild(row));
            });
        });
    });
});
