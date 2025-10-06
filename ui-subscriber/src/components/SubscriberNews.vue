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
      eventSource: null, // 🔹 En lugar de ws
    };
  },
  mounted() {
    this.cargarPublicaciones();
    this.conectarSSE(); // 🔹 Reemplaza al WebSocket
  },
  methods: {
    async cargarPublicaciones() {
      try {
        const response = await fetch("http://127.0.0.1:8001/");
        if (!response.ok) throw new Error("Error al obtener publicaciones");

        const data = await response.json();
        this.publicaciones = data.reverse(); // más recientes primero
        this.cargando = false;
        console.log("🧾 Publicaciones iniciales cargadas:", data);
      } catch (error) {
        console.error("❌ Error al cargar publicaciones:", error);
        this.mensaje = "❌ Error al cargar publicaciones iniciales";
        this.exito = false;
        this.cargando = false;
      }
    },

    // 🔹 Nuevo método para escuchar eventos SSE
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
        // Puedes parsear si viene en JSON
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
.form-container {
  max-width: 600px;
  margin: 50px auto;
  background-color: #f4f4f4;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #333;
}

.lista-noticias {
  list-style-type: none;
  padding: 0;
  margin-top: 15px;
}

.noticia {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 10px;
  transition: background-color 0.3s;
}

.noticia:hover {
  background-color: #e9f0ff;
}

.mensaje {
  text-align: center;
  margin-top: 15px;
  font-weight: bold;
}

.mensaje.exito {
  color: #28a745;
}

.mensaje.error {
  color: #dc3545;
}

.mensaje.info {
  color: #007bff;
}
</style>
