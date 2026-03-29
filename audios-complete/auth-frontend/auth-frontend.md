# Transcripcion: auth-frontend.mp3

## Metadatos
- **Archivo original:** auth-frontend.mp3
- **Fecha de transcripcion:** 2026-02-18 10:26:12
- **Modelo utilizado:** gpt-4o-transcribe

---

## Transcripcion

Entonces, quiero implementar el login ya con el backend. Entonces, esta es la idea desde el lado del frontend, donde actualmente tenemos prototipado email y contraseña y un botón de Google. Vamos a implementar solamente que se logue con el celular. Entonces, debe tener un selector de país, debe tener el input del celular, instalar esa librería, iniciar sesión. El registro lo hacemos desde el administrador del backend. Entonces, no vamos a implementar registro. Luego de que haga login, vamos a hacer dos cosas. Una, vamos a mejorar el comportamiento del navbar. Está muy transparente, no debería ser transparente y que va a estar colapsado desde un principio para que siempre no aterrice o cada vez que cambie de página no esté abierto. Luego de eso, vamos a poder habilitar el botón de cerrar sesión y antes de cargar debe llamar el endpoint de el dashme, que va a traer la información de las organizaciones. Por defecto, si tiene una sola organización, se le selecciona esa organización. Entonces, todo empezar desde ahí con el frontend para empezar a setear organizaciones. Pero de entrada vamos a dejarlo. Entonces, esa es la idea, ese es el backlog, autenticación, login, cerrar sesión, mejorar el comportamiento del navbar, el frontend y poder seleccionar organización que por defecto, pues de entrada vamos a manejar una organización, van a ir a la lista y esa debe ser la seleccionada. Ahí tiene que comunicarte con el backend para traer esos endpoints para poder listarlos sin ningún problema. Solamente revisa entre el backend para que implementes esto en el frontend. El resto en el frontend lo hace igual todo prototipado, todo moqueado, que ya vamos a ir creando esos nuevos ciclos.

---

*Generado automaticamente con OpenAI API*
