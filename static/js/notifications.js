const notificationSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notifications/'
);

notificationSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    updateNotificationBadges(data.message);
};

function updateNotificationBadges(data) {
    Object.keys(data).forEach(tipo => {
        const badge = document.querySelector(`#badge-${tipo}`);
        if (badge) {
            if (data[tipo] > 0) {
                badge.textContent = data[tipo];
                badge.style.display = 'inline';
            } else {
                badge.style.display = 'none';
            }
        }
    });
} 