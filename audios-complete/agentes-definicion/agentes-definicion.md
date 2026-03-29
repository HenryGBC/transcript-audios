# Transcripcion: agentes-definicion.mp3

## Metadatos
- **Archivo original:** agentes-definicion.mp3
- **Fecha de transcripcion:** 2026-02-18 17:56:12
- **Modelo utilizado:** gpt-4o-transcribe

---

## Transcripcion

Listo. Vamos a definir la parte de los agentes. Entonces, vamos a definirlo por partes. Antes de empezar a definir los agentes, que si vamos a crear las tools, las skills, entre muchas cosas más, definamos primero desde lo básico. Vamos a definir primero una experiencia de agentes empleados básicos con las instrucciones, manejar el historial de conversaciones, mensajes tipo user, mensajes tipo assistant, totalmente básicos. Pero, ¿qué me imagino? Me imagino que por defecto, desde el admin, nosotros configuremos estos empleados. Se le asigna un empleado al branch, se le asigna un empleado, sí, por branch, a la organización, el empleado operativo y el empleado de la cara al cliente. Ambos van a tener instrucciones predeterminadas que se manejarán desde el backend, desde el admin, y se les concatenará con texto en algún lado. Entonces, tiene que haber una tabla de contexto del negocio, contexto completo. ¿Qué otra cosa? Luego de eso que definamos esta experiencia, para poder abordar esto desde el frontend, vamos a, esto es como para la parte del backend, como de inicial. Luego la parte del frontend, lo que vamos a hacer es, primero vamos a ver en el inicio los empleados, vamos a poder esto, vamos a poder ver el historial de las conversaciones por empleados, si lo pueda tomar después un humano o no, ya lo revisaremos con el tema de WhatsApp, pero de entrada vamos a poder ver el historial de conversaciones que han tenido estos empleados. Para interactuar con estos empleados, actualmente vamos a hacer, antes de pensar en WhatsApp, vamos a poner un canal de web, que es el estándar normal, y vamos a poder abrir ese empleado en una URL pública. Esa URL pública va a poder acceder cualquier persona, pero tiene que meter el número y loggearse. En el caso de empleado operativo, si no está loggeado, loggearse para acceder a esto. Entonces, en el caso del empleado operativo, no es tan público, sino loggearse y ahí sí poder interactuar con el empleado. Esto es para que siempre tenga la mano el empleado y no necesariamente tenga que entrar al dashboard, seleccionar el empleado, no, sino una URL, este es su empleado, puede hablar. No está loggeado, loggeese y ya puede interactuar con él, como un independiente. Y de cara al cliente, igual, pero el cliente no se loggea, sino pues mete el OTP como de manera de confirmación y inicia el contexto de la conversación con ese número celular. Ya luego pues con las herramientas y todo eso va a tener contexto que esa persona es un cliente o no es un cliente, etc. Pero eso ya es otra parte. Pero de entrada es la forma de interactuar con los empleados. Y bueno, los endpoints necesarios para la interacción con este empleado. Del lado del empleado operativo debe ser privado todo, del lado del cliente, del empleado cliente sí puede ser público, pero previamente validado por un OTP para asegurar que no haya spam por ahí. Listo.

---

*Generado automaticamente con OpenAI API*
