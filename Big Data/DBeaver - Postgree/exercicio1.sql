INSERT INTO fornecedores (nome_fornecedor, cnpj) VALUES 
('Tech Solutions', '12.345.678/0001-01'), ('Global Import', '23.456.789/0001-02'),
('Distribuidora Norte', '34.567.890/0001-03'), ('Logística Express', '45.678.901/0001-04'),
('Fábrica Real', '56.789.012/0001-05'), ('Peças & Cia', '67.890.123/0001-06'),
('Mega Atacado', '78.901.234/0001-07'), ('Suprimentos Sul', '89.012.345/0001-08'),
('Mundo Digital', '90.123.456/0001-09'), ('Parceiro Ideal', '01.234.567/0001-10');

INSERT INTO categorias_produtos (nome_categoria, valor_unitario) VALUES 
('Eletrônicos', 1500.00), ('Móveis', 800.00), ('Escritório', 50.00),
('Limpeza', 20.00), ('Alimentos', 15.00), ('Ferramentas', 120.00),
('Automotivo', 300.00), ('Vestuário', 90.00), ('Brinquedos', 60.00), ('Saúde', 45.00);

INSERT INTO produtos (nome_produto, valor_unitario, id_fornecedor, id_categoria_produtos) VALUES 
('Notebook Pro', 4500.00, 1, 1), ('Cadeira Gamer', 1200.00, 2, 2),
('Teclado Mecânico', 350.00, 1, 1), ('Papel A4', 25.00, 3, 3),
('Detergente 5L', 18.00, 4, 4), ('Arroz 5kg', 30.00, 5, 5),
('Martelo', 45.00, 6, 6), ('Pneu Aro 15', 400.00, 7, 7),
('Camiseta Algodão', 50.00, 8, 8), ('Lego City', 250.00, 9, 9);

INSERT INTO produtos (nome_produto, valor_unitario, id_fornecedor, id_categoria_produtos) VALUES 
('Notebook Pro', 4500.00, 1, 1), ('Cadeira Gamer', 1200.00, 2, 2),
('Teclado Mecânico', 350.00, 1, 1), ('Papel A4', 25.00, 3, 3),
('Detergente 5L', 18.00, 4, 4), ('Arroz 5kg', 30.00, 5, 5),
('Martelo', 45.00, 6, 6), ('Pneu Aro 15', 400.00, 7, 7),
('Camiseta Algodão', 50.00, 8, 8), ('Lego City', 250.00, 9, 9);

UPDATE fornecedores SET nome_fornecedor = 'Tech Solutions LTDA' WHERE id_fornecedor = 1;
UPDATE fornecedores SET cnpj = '00.000.000/0001-00' WHERE id_fornecedor = 10;

UPDATE categorias_produtos SET nome_categoria = 'Informática' WHERE id_categoria = 1;
UPDATE categorias_produtos SET valor_base_categoria = 100.00 WHERE id_categoria = 3;

UPDATE produtos SET valor_unitario = 4800.00 WHERE id_produto = 1;
UPDATE produtos SET nome_produto = 'Cadeira Ergonômica' WHERE id_produto = 2;

DELETE FROM produtos WHERE id_produto = 10;
DELETE FROM produtos WHERE id_produto = 9;
DELETE FROM produtos WHERE id_produto = 8;
DELETE FROM produtos WHERE id_produto = 7;
DELETE FROM produtos WHERE id_produto = 6;

DELETE FROM fornecedores WHERE id_fornecedor = 10;
DELETE FROM fornecedores WHERE id_fornecedor = 9;
DELETE FROM fornecedores WHERE id_fornecedor = 8;
DELETE FROM fornecedores WHERE id_fornecedor = 7;
DELETE FROM fornecedores WHERE id_fornecedor = 6;

DELETE FROM categorias_produtos WHERE id_categoria = 10;
DELETE FROM categorias_produtos WHERE id_categoria = 9;
DELETE FROM categorias_produtos WHERE id_categoria = 8;
DELETE FROM categorias_produtos WHERE id_categoria = 7;
DELETE FROM categorias_produtos WHERE id_categoria = 6;