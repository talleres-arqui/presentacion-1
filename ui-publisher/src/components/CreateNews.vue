<template>
  <div class="form-container">
    <h1>Crear Noticia</h1>

    <form @submit.prevent="enviarNoticia">
      <div class="campo">
        <label for="titulo">Título:</label>
        <input
          type="text"
          id="titulo"
          v-model="titulo"
          placeholder="Escribe el título de la noticia"
          required
        />
      </div>

      <div class="campo">
        <label for="body">Contenido:</label>
        <textarea
          id="body"
          v-model="body"
          placeholder="Escribe el cuerpo de la noticia"
          required
        ></textarea>
      </div>

      <button type="submit">Publicar</button>

      <p v-if="mensaje" class="mensaje">{{ mensaje }}</p>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CreateNews",
  data() {
    return {
      titulo: "",
      body: "",
      mensaje: ""
    };
  },
  methods: {
    async enviarNoticia() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/publication", {
          title: this.titulo,
          body: this.body,
        });
        this.mensaje = "✅ Noticia publicada con éxito";
        console.log(response.data);

        // Limpia el formulario
        this.titulo = "";
        this.body = "";
      } catch (error) {
        console.error("Error al publicar noticia:", error);
        this.mensaje = "❌ Error al publicar la noticia";
      }
    },
  },
};
</script>

<style scoped>
.form-container {
  max-width: 500px;
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

.campo {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

input,
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  font-size: 16px;
}

button:hover {
  background-color: #0056b3;
}

.mensaje {
  margin-top: 15px;
  text-align: center;
  font-weight: bold;
}
</style>
