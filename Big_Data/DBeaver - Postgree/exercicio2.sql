select max(preco_produto), min(preco_produto) from  produto
select count(*) from produto;
select count(*) from produto where preco_produto > 10;
select avg(preco_produto) from produto;
select sum(preco_produto) from produto;

select count(id_produto), id_categoria from produto group by id_categoria
select count(pro.id_produto), cat.desc_categoria
	from produto pro
	inner join categoria cat on pro.id_categoria = cat.id_categoria
	group by cat.id_categoria

select pro.*, cat.desc_categoria
		from produto pro
		inner join categoria cat on pro.id_categoria = cat.id_categoria;

select pro.*, cat.desc_categoria
		from produto pro
		left join categoria cat on pro.id_categoria = cat.id_categoria;

select pro.*, cat.desc_categoria
		from produto pro
		right join categoria cat on pro.id_categoria = cat.id_categoria;