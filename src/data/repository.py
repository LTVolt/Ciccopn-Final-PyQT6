from __future__ import annotations

from typing import Any

from .db import get_connection


class ImovelRepository:
    def listar_anunciantes(self) -> list[dict[str, Any]]:
        query = """
            SELECT
                a.id_anunciante,
                a.email,
                a.tipo,
                COALESCE(p.nome, c.nome, ag.nome, 'Sem nome') AS nome,
                CASE
                    WHEN a.tipo = 1 THEN 'Proprietário'
                    WHEN a.tipo = 2 THEN 'Consultor'
                    WHEN a.tipo = 3 THEN 'Agência'
                    ELSE CONCAT('Tipo ', a.tipo)
                END AS tipo_label
            FROM anunciante a
            LEFT JOIN proprietario p ON p.id_proprietario = a.id_proprietario
            LEFT JOIN consultor c ON c.id_consultor = a.id_consultor
            LEFT JOIN agencia ag ON ag.id_agencia = a.id_agencia
            ORDER BY email ASC
        """
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(query)
                return list(cur.fetchall())

    def listar_distritos(self) -> list[dict[str, Any]]:
        query = """
            SELECT id_distrito, nome
            FROM distrito
            ORDER BY nome ASC
        """
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(query)
                return list(cur.fetchall())

    def listar_concelhos_por_distrito(self, id_distrito: str) -> list[dict[str, Any]]:
        query = """
            SELECT id_concelho, nome
            FROM concelho
            WHERE id_distrito = %s
            ORDER BY nome ASC
        """
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(query, (id_distrito,))
                return list(cur.fetchall())

    def listar_freguesias_por_concelho(self, id_concelho: str) -> list[dict[str, Any]]:
        query = """
            SELECT id_freguesia, nome
            FROM freguesia
            WHERE id_concelho = %s
            ORDER BY nome ASC
        """
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(query, (id_concelho,))
                return list(cur.fetchall())

    def listar_imoveis(self, limit: int = 200) -> list[dict[str, Any]]:
        query = """
            SELECT
                i.id_imovel,
                i.morada,
                i.preco,
                i.numero_quartos,
                i.numero_wc,
                i.area,
                f.nome AS freguesia,
                c.nome AS concelho,
                d.nome AS distrito,
                i.data_anuncio
            FROM imovel i
            LEFT JOIN freguesia f ON f.id_freguesia = i.id_freguesia
            LEFT JOIN concelho c ON c.id_concelho = f.id_concelho
            LEFT JOIN distrito d ON d.id_distrito = c.id_distrito
            ORDER BY i.data_anuncio DESC
            LIMIT %s
        """
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(query, (limit,))
                return list(cur.fetchall())

    def pesquisar_imoveis(
        self,
        texto: str,
        preco_max: float | None = None,
        id_distrito: str | None = None,
        id_concelho: str | None = None,
        id_freguesia: str | None = None,
    ) -> list[dict[str, Any]]:
        filtros = ["(i.morada LIKE %s OR i.descricao LIKE %s)"]
        params: list[Any] = [f"%{texto}%", f"%{texto}%"]

        if preco_max is not None:
            filtros.append("i.preco <= %s")
            params.append(preco_max)

        if id_distrito:
            filtros.append("d.id_distrito = %s")
            params.append(id_distrito)

        if id_concelho:
            filtros.append("c.id_concelho = %s")
            params.append(id_concelho)

        if id_freguesia:
            filtros.append("f.id_freguesia = %s")
            params.append(id_freguesia)

        query = f"""
            SELECT
                i.id_imovel,
                i.morada,
                i.preco,
                i.numero_quartos,
                i.numero_wc,
                i.area,
                f.nome AS freguesia,
                c.nome AS concelho,
                d.nome AS distrito,
                i.data_anuncio
            FROM imovel i
            LEFT JOIN freguesia f ON f.id_freguesia = i.id_freguesia
            LEFT JOIN concelho c ON c.id_concelho = f.id_concelho
            LEFT JOIN distrito d ON d.id_distrito = c.id_distrito
            WHERE {' AND '.join(filtros)}
            ORDER BY i.data_anuncio DESC
            LIMIT 200
        """
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(query, tuple(params))
                return list(cur.fetchall())

    def criar_anuncio(self, payload: dict[str, Any]) -> int:
        query = """
            INSERT INTO imovel (
                morada,
                preco,
                descricao,
                numero_quartos,
                numero_wc,
                data_construcao,
                area,
                id_anunciante,
                id_freguesia
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            payload["morada"],
            payload["preco"],
            payload.get("descricao"),
            payload.get("numero_quartos", 0),
            payload.get("numero_wc", 0),
            payload.get("data_construcao"),
            payload["area"],
            payload["id_anunciante"],
            payload["id_freguesia"],
        )

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, values)
                conn.commit()
                return int(cur.lastrowid)
