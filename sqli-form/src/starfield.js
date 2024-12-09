const canvas = document.getElementById('starfield');
const ctx = canvas.getContext('2d', { alpha: false });

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();

const stars = [];
const numStars = 400;
const centerX = canvas.width / 2;
const centerY = canvas.height / 2;

class Star {
    constructor() {
        this.reset();
    }
    
    reset() {
        this.x = Math.random() * canvas.width - centerX;
        this.y = Math.random() * canvas.height - centerY;
        this.z = Math.random() * 1500;
        this.opacity = 0;
    }
    
    update() {
        this.z -= 10;
        this.opacity = Math.min(this.z / 1000, 1);
        
        if (this.z <= 0) {
            this.reset();
        }
        
        const k = 128 / this.z;
        const px = this.x * k + centerX;
        const py = this.y * k + centerY;
        
        if (px < 0 || px > canvas.width || py < 0 || py > canvas.height) {
            this.reset();
        }
        
        return {
            x: px,
            y: py,
            size: k,
            opacity: this.opacity
        };
    }
}

// Создаем звезды
for (let i = 0; i < numStars; i++) {
    stars.push(new Star());
}

function draw() {
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    stars.forEach(star => {
        const pos = star.update();
        const size = Math.min(pos.size, 3);
        
        ctx.beginPath();
        ctx.fillStyle = `rgba(255, 0, 0, ${pos.opacity})`;
        ctx.arc(pos.x, pos.y, size, 0, Math.PI * 2);
        ctx.fill();
    });
    
    requestAnimationFrame(draw);
}

draw();

window.addEventListener('resize', () => {
    resizeCanvas();
    centerX = canvas.width / 2;
    centerY = canvas.height / 2;
});
