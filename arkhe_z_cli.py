#!/usr/bin/env python3
import click
import requests
import json
import yaml

@click.group()
def cli():
    """ARKHE-Z CLI — Interação com a Blockchain Z via Bridge"""
    pass

@cli.command()
@click.option('--sequence', required=True, help='Sequência canônica (36 bits)')
@click.option('--bridge-url', default='http://localhost:8700', help='URL da Bridge API')
@click.option('--format', 'fmt', type=click.Choice(['json', 'yaml']), default='json', help='Formato de saída')
def publish(sequence, bridge_url, fmt):
    """Publica a sequência na blockchain através da Bridge e exibe o decreto."""
    payload = {"sequence": sequence, "metadata": {"glosa": "245", "n": 5, "k": 2}}
    try:
        resp = requests.post(f"{bridge_url}/publish", json=payload)
        resp.raise_for_status()
        receipt = resp.json()
        # Gera o decreto estruturado
        decree = {
            "substrate": "870-B-GLOSA245",
            "action": "ANCHORED",
            "tx_hash": receipt["tx_hash"],
            "sequence_hash": receipt["sequence_hash"],
            "sequence": receipt["sequence"],
            "block_number": receipt["block_number"],
            "phi_c": 0.850,
            "ghost_threshold": 0.577,
            "metadata": receipt.get("metadata", {}),
            "timestamp": "2026-05-26T00:00:00Z",
            "keeper": "ψ"
        }
        if fmt == 'yaml':
            print(yaml.dump(decree, allow_unicode=True, sort_keys=False))
        else:
            print(json.dumps(decree, indent=2, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        click.echo(f"Erro na comunicação com a Bridge: {e}")

if __name__ == "__main__":
    cli()
