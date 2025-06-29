 // Función para manejar click en módulo
    function selectModulo(nombreModulo, moduloId) {
        const cards = document.querySelectorAll('.modulo-card');
        const clickedCard = event.currentTarget;
        
        // Efecto de click
        clickedCard.style.transform = 'scale(0.95)';
        
        // Crear efecto de partículas
        createCardParticles(clickedCard);
        
        // Vibración si está disponible
        if (navigator.vibrate) {
            navigator.vibrate(50);
        }
        
        // Sonido de click
        playCardClickSound();
        
        // Restaurar transform después del efecto
        setTimeout(() => {
            clickedCard.style.transform = '';
        }, 200);
        
        // Mostrar mensaje motivacional
        setTimeout(() => {
            alert(`¡Genial elección! 🎉\n"${nombreModulo}"\n¡Prepárate para aprender y divertirte! 🌟`);
        }, 300);
    }

    // Crear efecto de partículas para tarjetas
    function createCardParticles(element) {
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        for (let i = 0; i < 6; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: fixed;
                width: 12px;
                height: 12px;
                background: linear-gradient(45deg, #667eea, #764ba2);
                border-radius: 50%;
                pointer-events: none;
                z-index: 1000;
                left: ${centerX}px;
                top: ${centerY}px;
            `;
            
            document.body.appendChild(particle);
            
            const angle = (Math.PI * 2 * i) / 6;
            const velocity = 80 + Math.random() * 40;
            const vx = Math.cos(angle) * velocity;
            const vy = Math.sin(angle) * velocity;
            
            particle.animate([
                { 
                    transform: 'translate(0, 0) scale(1)', 
                    opacity: 1 
                },
                { 
                    transform: `translate(${vx}px, ${vy}px) scale(0)`, 
                    opacity: 0 
                }
            ], {
                duration: 1000,
                easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
            }).onfinish = () => {
                document.body.removeChild(particle);
            };
        }
    }

    // Sonido de click para tarjetas
    function playCardClickSound() {
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.setValueAtTime(600, audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(900, audioContext.currentTime + 0.1);
            
            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.1);
        } catch (e) {
            // Silencioso si no se puede reproducir sonido
        }
    }

    // Efectos adicionales al cargar la página
    document.addEventListener('DOMContentLoaded', function() {
        // Añadir efectos de hover mejorados
        document.querySelectorAll('.modulo-card').forEach((card, index) => {
            card.addEventListener('mouseenter', function() {
                // Efecto de brillo adicional
                this.style.boxShadow = `
                    0 25px 50px rgba(0, 0, 0, 0.2),
                    0 10px 20px rgba(0, 0, 0, 0.1),
                    0 0 30px rgba(102, 126, 234, 0.3)
                `;
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.boxShadow = '';
            });
        });

        // Efecto de entrada para los botones
        document.querySelectorAll('.btn-jugar').forEach((btn, index) => {
            btn.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-3px) scale(1.05)';
            });
            
            btn.addEventListener('mouseleave', function() {
                this.style.transform = '';
            });
        });
    });