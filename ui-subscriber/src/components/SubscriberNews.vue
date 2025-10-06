<template>
  <div class="form-container">
    <h1>📰 Noticias Recibidas</h1>

    <div v-if="cargando" class="mensaje info">Cargando publicaciones...</div>

    <ul v-else class="lista-noticias">
      <li v-for="(pub, index) in publicaciones" :key="index" class="noticia">
        <h3>{{ pub.title }}</h3>
        <p>{{ pub.body }}</p>
      </li>
    </ul>

    <p v-if="mensaje" class="mensaje" :class="{ exito: exito, error: !exito }">
      {{ mensaje }}
    </p>
  </div>
</template>

<script>
export default {
  name: "SubscriberNews",
  data() {
    return {
      publicaciones: [],
      mensaje: "",
      cargando: true,
      exito: false,
      eventSource: null,
    };
  },
  mounted() {
    this.cargarPublicaciones();
    this.conectarSSE();
  },
  methods: {
    async cargarPublicaciones() {
      try {
        const response = await fetch("http://127.0.0.1:8001/");
        if (!response.ok) throw new Error("Error al obtener publicaciones");

        const data = await response.json();
        this.publicaciones = data.reverse();
        this.cargando = false;
        console.log("🧾 Publicaciones iniciales cargadas:", data);
      } catch (error) {
        console.error("❌ Error al cargar publicaciones:", error);
        this.mensaje = "❌ Error al cargar publicaciones iniciales";
        this.exito = false;
        this.cargando = false;
      }
    },
    conectarSSE() {
      const url = "http://127.0.0.1:8001/stream";
      console.log("📡 Conectando a SSE:", url);

      this.eventSource = new EventSource(url);

      this.eventSource.onopen = () => {
        console.log("✅ Conectado al servidor SSE");
        this.mensaje = "Conectado al servidor en tiempo real";
        this.exito = true;
      };

      this.eventSource.onmessage = (event) => {
        console.log("📩 Nuevo mensaje recibido:", event.data);
        try {
          const data = JSON.parse(event.data);
          this.publicaciones.unshift(data);
        } catch {
          this.publicaciones.unshift({
            title: "Actualización",
            body: event.data,
          });
        }
      };

      this.eventSource.onerror = (error) => {
        console.error("⚠️ Error en SSE:", error);
        this.mensaje = "Error en la conexión SSE";
        this.exito = false;
      };
    },
  },
  beforeUnmount() {
    if (this.eventSource) {
      this.eventSource.close();
      console.log("🔌 Conexión SSE cerrada");
    }
  },
};
</script>

<style scoped>
/* 🌙 Fondo general y centrado */
body {
  background: linear-gradient(135deg, #0f172a, #1e293b);
  color: #e2e8f0;
  font-family: 'Segoe UI', Roboto, sans-serif;
  min-height: 100vh;
}

/* 📦 Contenedor principal */
.form-container {
  max-width: 700px;
  margin: 50px auto;
  background: #1e293b;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
  color: #f8fafc;
}

/* 📰 Título */
h1 {
  text-align: center;
  color: #38bdf8;
  font-size: 2rem;
  margin-bottom: 20px;
  text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
}

/* 📋 Lista de noticias */
.lista-noticias {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

/* 🗞️ Tarjeta de cada noticia */
.noticia {
  background: #f8fafc;
  color: #0f172a;
  border-radius: 10px;
  padding: 15px 20px;
  margin-bottom: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  word-wrap: break-word;
  transition: all 0.3s ease;
}

.noticia:hover {
  background-color: #e0f2fe;
  transform: translateY(-3px);
}

/* 📄 Título de la noticia */
.noticia h3 {
  color: #0f172a;
  margin-bottom: 5px;
  font-weight: 700;
}

/* 📖 Texto del cuerpo */
.noticia p {
  font-size: 0.95rem;
  color: #1e293b;
  line-height: 1.5;
  word-break: break-word;
}

/* ℹ️ Mensajes */
.mensaje {
  text-align: center;
  margin-top: 20px;
  font-weight: bold;
  font-size: 1rem;
  border-radius: 10px;
  padding: 10px;
}

.mensaje.exito {
  color: #22c55e;
}

.mensaje.error {
  color: #ef4444;
}

.mensaje.info {
  color: #38bdf8;
}

/* 📱 Responsive */
@media (max-width: 768px) {
  .form-container {
    margin: 20px;
    padding: 20px;
  }

  h1 {
    font-size: 1.5rem;
  }

  .noticia p {
    font-size: 0.9rem;
  }
}
</style>
