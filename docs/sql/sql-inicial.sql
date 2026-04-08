create table rede (
	id_rede int not null auto_increment,
    nome varchar(999) not null,
    primary key (id_rede)
);

create table agencia (
	id_agencia int not null auto_increment,
    nome varchar(999) not null,
    id_rede int,
    primary key (id_agencia),
    foreign key (id_rede) references Rede(id_rede)
);

create table consultor (
	id_consultor int auto_increment primary key,
    nome varchar(999) not null,
    id_agencia int,
    foreign key (id_agencia) references agencia(id_agencia)
);

create table proprietario (
	id_proprietario int primary key,
    nome varchar(999) not null
);

create table distrito (
	id_distrito varchar(9) primary key,
    nome varchar(999) not null
);

create table concelho (
	id_concelho varchar(9) primary key,
    nome varchar(999) not null,
    id_distrito varchar(9),
    foreign key (id_distrito) references distrito(id_distrito)
);

create table freguesia (
	id_freguesia varchar(9) primary key,
    nome varchar(999) not null,
    id_concelho varchar(9),
    foreign key (id_concelho) references concelho(id_concelho)
);

create table anunciante (
	id_anunciante int auto_increment primary key,
    email varchar(999) not null,
	telefone varchar(999) not null,
    tipo int not null,
    id_proprietario int,
    id_consultor int,
    id_agencia int,
    foreign key (id_proprietario) references proprietario(id_proprietario),
    foreign key (id_agencia) references agencia(id_agencia),
    foreign key (id_consultor) references consultor(id_consultor)
);

create table imovel (
	id_imovel int auto_increment primary key,
    morada varchar(150) not null,
    data_anuncio datetime default current_timestamp,
    preco decimal(12,2) not null,
    descricao varchar(9999),
    numero_quartos int unsigned default 0,
    numero_wc int unsigned default 0,
    data_construcao date,
    area decimal(6,2) not null,
    id_anunciante int not null,
    id_freguesia int not null,
    foreign key (id_anunciante) references anunciante(id_anunciante),
    foreign key (id_freguesia) references freguesia(id_freguesia)
);