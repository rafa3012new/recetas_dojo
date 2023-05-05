create database recetas_dojo;

use recetas_dojo;

 CREATE TABLE IF NOT EXISTS `usuarios` (
   `id` int NOT NULL AUTO_INCREMENT,
   `usuario` varchar(255) NOT NULL,
   `password` varchar(255) NOT NULL,
   `nombre` varchar(255) NOT NULL,
   `apellido` varchar(255) NOT NULL,
   `email` varchar(255) NOT NULL,
   `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
   `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (`id`)
 ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


 CREATE TABLE IF NOT EXISTS `recetas` (
   `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
   `autor` int NOT NULL,
   `nombre` varchar(255) NOT NULL,
   `descripcion` varchar(255) NOT NULL,
   `instrucciones` varchar(255) NOT NULL,
   `under30` tinyint not null,
   `date_made` datetime not null,
   `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
   `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   CONSTRAINT `FK_Receta_Autor` FOREIGN KEY (`autor`) REFERENCES `usuarios` (`id`)
 ) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;