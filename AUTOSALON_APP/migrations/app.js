document.addEventListener("DOMContentLoaded", function () {
    const carGrid = document.getElementById("car-grid");
    const loadBtn = document.getElementById("load-cars-btn");
    
    const modal = document.getElementById("test-drive-modal");
    const closeBtn = document.getElementById("close-modal-btn");
    const tdForm = document.getElementById("test-drive-form");
    const tdFeedback = document.getElementById("td-feedback");

    async function fetchCars() {
        if (!carGrid) return;
        carGrid.innerHTML = '<div class="hud-empty" style="grid-column: 1 / -1;">// СКАНИРОВАНИЕ БАЗЫ ДАННЫХ...</div>';

        try {
            const response = await fetch('/api/cars/');
            if (!response.ok) throw new Error('Ошибка сети');
            const cars = await response.json();

            if (cars.length === 0) {
                carGrid.innerHTML = '<div class="hud-empty" style="grid-column: 1 / -1;">// БАЗА ДАННЫХ ПУСТА</div>';
                return;
            }

            carGrid.innerHTML = '';
            cars.forEach(car => {
                const card = document.createElement('article');
                card.className = 'car-card';
                const formattedPrice = parseFloat(car.price).toLocaleString('ru-RU');
                let imgHtml = car.image ? `<img src="${car.image}" alt="${car.brand_name}">` : `<div class="car-image-placeholder">NO IMAGE</div>`;
                
                const testDriveBtn = car.status === 'available' 
                    ? `<button class="btn-test-drive" data-id="${car.id}" data-name="${car.brand_name} ${car.model_name}">ТЕСТ-ДРАЙВ</button>` 
                    : '';

                card.innerHTML = `
                    <div class="car-image-wrap">
                        ${imgHtml}
                        <span class="car-card-id">ID #${car.id}</span>
                    </div>
                    <div class="car-body">
                        <div class="car-title">
                            <span class="car-brand">${car.brand_name}</span><br>${car.model_name}
                        </div>
                        <div class="car-specs">
                            <div class="car-spec-row"><span class="car-spec-key">Год</span><span class="car-spec-value">${car.year}</span></div>
                            <div class="car-spec-row"><span class="car-spec-key">Цвет</span><span class="car-spec-value">${car.color}</span></div>
                            <div class="car-spec-row"><span class="car-spec-key">Статус</span><span class="car-spec-value"><span class="status-badge status-${car.status}">${car.status_display}</span></span></div>
                        </div>
                        <div class="car-price">${formattedPrice} ₽</div>
                        ${testDriveBtn}
                    </div>
                `;
                carGrid.appendChild(card);
            });

            document.querySelectorAll('.btn-test-drive').forEach(btn => {
                btn.addEventListener('click', function() {
                    const carId = this.getAttribute('data-id');
                    const carName = this.getAttribute('data-name');
                    
                    document.getElementById('td-car-id').value = carId;
                    document.getElementById('td-car-name').textContent = carName;
                    tdFeedback.innerHTML = '';
                    tdForm.reset();
                    
                    modal.style.display = 'flex';
                });
            });

        } catch (error) {
            carGrid.innerHTML = '<div class="hud-message hud-message-error" style="grid-column: 1 / -1;">▮ ОШИБКА ПОДКЛЮЧЕНИЯ К API</div>';
        }
    }

    tdForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(tdForm);
        const data = {
            car: formData.get('car'),
            client_name: formData.get('client_name'),
            client_phone: formData.get('client_phone'),
            date_time: formData.get('date_time')
        };

        try {
            const response = await fetch('/api/test-drives/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                tdFeedback.innerHTML = '<div class="hud-message">▮ ЗАПИСЬ ПОДТВЕРЖДЕНА. ЖДИТЕ ЗВОНКА.</div>';
                setTimeout(() => { modal.style.display = 'none'; }, 2000);
            } else {
                tdFeedback.innerHTML = `<div class="hud-message hud-message-error">▮ ОШИБКА ВАЛИДАЦИИ</div>`;
            }
        } catch (error) {
            tdFeedback.innerHTML = '<div class="hud-message hud-message-error">▮ ОШИБКА СЕТИ</div>';
        }
    });

    closeBtn.addEventListener('click', () => modal.style.display = 'none');
    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    if (loadBtn) loadBtn.addEventListener("click", (e) => { e.preventDefault(); fetchCars(); });
    fetchCars();
});