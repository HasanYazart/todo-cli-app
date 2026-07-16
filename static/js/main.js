// Pomodoro
let t = (typeof DEFAULT_POMO_TIME !== 'undefined') ? DEFAULT_POMO_TIME * 60 : 1500;
let i;
function upd() {
    let m = Math.floor(t/60), s = t%60;
    document.getElementById("timer").innerText = m + ":" + ("0"+s).slice(-2);
}
function setTime(m) { t = m * 60; upd(); pause(); }
function start() {
    if(i) return;
    i = setInterval(() => {
        t--; upd();
        if(t <= 0) { 
            clearInterval(i); 
            document.getElementById("sound").play(); 
            Swal.fire({
                title: 'Süre Doldu!',
                text: 'Pomodoro seansınız tamamlandı, tebrikler!',
                icon: 'success',
                confirmButtonColor: 'var(--accent-1)',
                background: 'var(--bg-card)',
                color: 'var(--text-main)'
            });
            reset(); 
        }
    }, 1000);
}
function pause() { clearInterval(i); i = null; }
function reset() { pause(); t = (typeof DEFAULT_POMO_TIME !== 'undefined') ? DEFAULT_POMO_TIME * 60 : 1500; upd(); }
upd();

// Edit toggle
function toggleEdit(id) {
    const f = document.getElementById('edit-form-' + id);
    f.style.display = f.style.display === 'flex' ? 'none' : 'flex';
}

// Delete
async function deleteTask(taskId) {
    const result = await Swal.fire({
        title: 'Emin misiniz?',
        text: "Görevi kalıcı olarak silmek istediğinize emin misiniz?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: 'var(--danger)',
        cancelButtonColor: 'var(--bg-card-solid)',
        confirmButtonText: 'Evet, Sil!',
        cancelButtonText: 'İptal',
        background: 'var(--bg-card)',
        color: 'var(--text-main)'
    });
    if(!result.isConfirmed) return;

    const res = await fetch(`/api/delete/${taskId}`, {
        method: 'POST',
        headers: {'X-CSRF-Token': CSRF_TOKEN}
    });
    if((await res.json()).status === "success") {
        const card = document.getElementById(`task-card-${taskId}`);
        card.style.transform = "scale(0.95) translateY(-10px)";
        card.style.opacity = "0";
        setTimeout(() => card.remove(), 350);
    }
}

// Toggle main task
async function toggleMainTask(taskId) {
    const res = await fetch(`/api/done/${taskId}`, {
        method: 'POST',
        headers: {'X-CSRF-Token': CSRF_TOKEN}
    });
    const data = await res.json();
    if(data.status === "success") {
        const btn = document.getElementById(`btn-main-${taskId}`);
        const card = document.getElementById(`task-card-${taskId}`);
        card.setAttribute("data-done", data.is_done ? "1" : "0");
        if(data.is_done) {
            btn.classList.add('active');
            card.classList.add('is-done');
        } else {
            btn.classList.remove('active');
            card.classList.remove('is-done');
        }
    }
}

// Toggle subtask
async function toggleSubtask(subId, taskId) {
    const res = await fetch(`/api/toggle/${subId}`, {
        method: 'POST',
        headers: {'X-CSRF-Token': CSRF_TOKEN}
    });
    const data = await res.json();
    if(data.status === "success") {
        const btn = document.getElementById(`sub-btn-${subId}`);
        const text = document.getElementById(`sub-text-${subId}`);
        const pFill = document.getElementById(`progress-fill-${taskId}`);
        const pText = document.getElementById(`progress-text-${taskId}`);
        if(data.is_done) {
            btn.innerHTML = '<i class="fa-solid fa-circle-check" style="color: var(--success);"></i>';
            text.classList.add("done");
        } else {
            btn.innerHTML = '<i class="fa-regular fa-circle"></i>';
            text.classList.remove("done");
        }
        pFill.style.width = `${data.percent}%`;
        pText.innerText = `%${data.percent}`;
        if(data.percent === 100) pFill.classList.add('complete');
        else pFill.classList.remove('complete');
    }
}

// Search
function searchTasks() {
    const input = document.getElementById('search-input').value.toLowerCase();
    const activeFilter = document.querySelector('.filter-btn.active').id.replace('filter-', '');
    
    document.querySelectorAll('.task-card').forEach(card => {
        const title = card.querySelector('.task-title').innerText.toLowerCase();
        let isDone = card.getAttribute('data-done') === '1';
        let showByFilter = true;
        
        if(activeFilter === 'todo' && isDone) showByFilter = false;
        if(activeFilter === 'done' && !isDone) showByFilter = false;
        
        if (title.includes(input) && showByFilter) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Filter
function filterTasks(type, btn) {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    searchTasks();
}

document.addEventListener('DOMContentLoaded', () => {
    // Set min date for deadline inputs
    const today = new Date().toISOString().split('T')[0];
    document.querySelectorAll('input[type="date"][name="deadline"]').forEach(el => {
        el.setAttribute('min', today);
    });

    const el = document.getElementById('tasks-container');
    if (el) {
        new Sortable(el, {
            animation: 150,
            handle: '.handle',
            onEnd: async function () {
                const ids = Array.from(el.querySelectorAll('.task-card'))
                    .map(card => Number(card.id.replace('task-card-', '')))
                    .filter(Number.isInteger);
                await fetch('/api/reorder', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-Token': CSRF_TOKEN
                    },
                    body: JSON.stringify({order: ids})
                });
            }
        });
    }
});
