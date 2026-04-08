-- Correção para alinhar tipos entre imovel.id_freguesia e freguesia.id_freguesia
-- O tipo em freguesia é VARCHAR(9), logo em imovel também deve ser VARCHAR(9).

ALTER TABLE imovel
    DROP FOREIGN KEY imovel_ibfk_2;

ALTER TABLE imovel
    MODIFY COLUMN id_freguesia VARCHAR(9) NOT NULL;

ALTER TABLE imovel
    ADD CONSTRAINT fk_imovel_freguesia
    FOREIGN KEY (id_freguesia)
    REFERENCES freguesia(id_freguesia);
