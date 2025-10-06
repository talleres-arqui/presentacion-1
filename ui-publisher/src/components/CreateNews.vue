<template>
  <div class="container">
    <div class="card">
      <div class="header">
        <div class="header-content">
          <svg
            class="icon"
            xmlns="http://www.w3.org/2000/svg"
            width="32"
            height="32"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"
            />
            <path d="M18 14h-8" />
            <path d="M15 18h-5" />
            <path d="M10 6h8v4h-8z" />
          </svg>
          <h1>Publicar Noticia</h1>
        </div>
        <p class="subtitle">Comparte las últimas noticias con tu audiencia</p>
      </div>

      <form @submit.prevent="publicarNoticia">
        <div class="form-group">
          <label for="title">Título de la Noticia</label>
          <input
            v-model="titulo"
            type="text"
            id="title"
            placeholder="Ingresa un título llamativo..."
            required
          />
        </div>

        <div class="form-group">
          <label for="body">Contenido</label>
          <textarea
            v-model="contenido"
            id="body"
            rows="12"
            placeholder="Escribe el contenido de la noticia..."
            required
          ></textarea>
        </div>

        <div class="form-footer">
          <div class="char-count">
            <span v-if="titulo.length > 0">
              Título: {{ titulo.length }} caracteres
            </span>
          </div>
          <button type="submit" class="submit-btn">
            <svg
              class="btn-icon"
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <line x1="22" y1="2" x2="11" y2="13" />
              <polygon points="22 2 15 22 11 13 2 9 22 2" />
            </svg>
            Publicar Noticia
          </button>
        </div>
      </form>
    </div>

    <div class="footer-note">
      <p>Asegúrate de revisar tu noticia antes de publicar</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "PublisherNews",
  data() {
    return {
      titulo: "",
      contenido: "",
    };
  },
  methods: {
    async publicarNoticia() {
      if (!this.titulo.trim() || !this.contenido.trim()) {
        alert("Por favor completa todos los campos antes de publicar.");
        return;
      }

      const noticia = {
        title: this.titulo,
        body: this.contenido,
      };

      try {
        console.log("📤 Publicando noticia:", noticia);
        // 👉 Aquí mandas la noticia al backend FastAPI que publica por MQTT
        const response = await fetch("http://127.0.0.1:8000/publication", {
      method: "POST",
      headers: {
      "Content-Type": "application/json",
      },
     body: JSON.stringify(noticia),
        });

        if (!response.ok) throw new Error("Error al publicar la noticia");

        alert("✅ ¡Noticia publicada con éxito!");
        this.titulo = "";
        this.contenido = "";
      } catch (error) {
        console.error("❌ Error al publicar:", error);
        alert("❌ Error al publicar la noticia.");
      }
    },
  },
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    'Helvetica Neue', Arial, sans-serif;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  min-height: 100vh;
  padding: 3rem 1rem;
}

.container {
  max-width: 56rem;
  margin: 0 auto;
}

.card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

.header {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  padding: 2rem;
  color: white;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.icon {
  width: 2rem;
  height: 2rem;
}

.header h1 {
  font-size: 1.875rem;
  font-weight: 700;
}

.subtitle {
  color: #cbd5e1;
  margin-top: 0.5rem;
  font-size: 0.95rem;
}

form {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #334155;
  margin-bottom: 0.5rem;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  color: #0f172a;
  transition: all 0.2s ease;
  font-family: inherit;
}

input[type="text"]:focus,
textarea:focus {
  outline: none;
  border-color: #1e293b;
  background: white;
}

input[type="text"]::placeholder,
textarea::placeholder {
  color: #94a3b8;
}

textarea {
  resize: none;
}

.form-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 1rem;
}

.char-count {
  font-size: 0.875rem;
  color: #64748b;
}

.char-count span {
  display: inline-block;
  background: #f1f5f9;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
}

.submit-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #1e293b;
  color: white;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.submit-btn:hover {
  background: #0f172a;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
  transform: translateY(-2px);
}

.submit-btn:active {
  transform: translateY(0);
}

.btn-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.footer-note {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.875rem;
  color: #64748b;
}

@media (max-width: 640px) {
  body {
    padding: 1.5rem 1rem;
  }

  .header {
    padding: 1.5rem;
  }

  .header h1 {
    font-size: 1.5rem;
  }

  form {
    padding: 1.5rem;
  }

  .form-footer {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .char-count {
    text-align: center;
  }

  .submit-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
