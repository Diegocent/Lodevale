CREATE TABLE productos(id Serial, nombre text, precio int, cantidad int);
  
INSERT INTO productos(nombre, precio, cantidad) VALUES ('COCA', 15000,2 );
INSERT INTO productos(nombre, precio, cantidad) VALUES ('papas fritas', 12000,10 );

SELECT * FROM productos;
ALTER TABLE productos ADD COLUMN codigo;