"""Phase 3 CLI commands for search index management."""

import click
from flask.cli import with_appcontext
from app.models import SearchIndex, Material
from app.services.search_service import SearchService
from datetime import datetime


@click.command('rebuild-search-index')
@with_appcontext
def rebuild_search_index():
    """Rebuild the entire search index from published materials.
    
    This command will:
    1. Clear the current search index
    2. Re-index all published materials
    3. Report statistics on completion
    
    Use this after migrations or if the index becomes corrupted.
    """
    click.echo("Starting search index rebuild...")
    click.echo("This may take a while depending on the number of materials.")
    
    try:
        indexed, skipped, errors = SearchIndex.rebuild_index()
        
        click.secho(f"\n✓ Search index rebuild complete!", fg='green')
        click.echo(f"  Indexed:  {indexed}")
        click.echo(f"  Skipped:  {skipped}")
        click.echo(f"  Errors:   {errors}")
        
    except Exception as e:
        click.secho(f"\n✗ Error during index rebuild: {str(e)}", fg='red')


@click.command('search-stats')
@with_appcontext
def search_stats():
    """Display search index statistics and health information."""
    stats = SearchIndex.get_index_stats()
    
    click.echo("\n" + "="*50)
    click.secho("Search Index Statistics", fg='cyan', bold=True)
    click.echo("="*50)
    
    click.echo(f"Total Indexed:    {stats.get('total_indexed', 0)}")
    click.echo(f"Total Unindexed:  {stats.get('total_unindexed', 0)}")
    
    if stats.get('last_updated'):
        click.echo(f"Last Updated:     {stats['last_updated']}")
    
    if stats.get('by_type'):
        click.echo("\nBy File Type:")
        for file_type, count in sorted(stats['by_type'].items()):
            click.echo(f"  {file_type:10} {count:5} items")
    
    total_materials = Material.query.count()
    published = Material.query.filter_by(is_published=True).count()
    indexed = stats.get('total_indexed', 0)
    
    click.echo("\nIndex Coverage:")
    click.echo(f"  Total Materials:   {total_materials}")
    click.echo(f"  Published:         {published}")
    click.echo(f"  Indexed:           {indexed}")
    
    if published > 0:
        coverage = (indexed / published) * 100
        if coverage >= 95:
            click.secho(f"  Coverage:          {coverage:.1f}% ✓", fg='green')
        elif coverage >= 80:
            click.secho(f"  Coverage:          {coverage:.1f}% ⚠", fg='yellow')
        else:
            click.secho(f"  Coverage:          {coverage:.1f}% ✗", fg='red')
    
    click.echo("="*50 + "\n")


@click.command('search-test')
@click.option('--query', prompt='Search query', help='Test search query')
@with_appcontext
def search_test(query):
    """Test the search functionality with a sample query."""
    click.echo(f"\nSearching for: '{query}'")
    click.echo("Please wait...\n")
    
    try:
        total, results = SearchIndex.search(query, limit=10)
        
        click.secho(f"Found {total} results:", fg='cyan', bold=True)
        
        if not results:
            click.secho("No results found.", fg='yellow')
        else:
            for i, result in enumerate(results, 1):
                click.echo(f"\n{i}. {result.title}")
                click.echo(f"   Course: {result.course_name}")
                if result.module_name:
                    click.echo(f"   Module: {result.module_name}")
                click.echo(f"   Type: {result.file_type}")
                click.echo(f"   By: {result.uploaded_by_name}")
        
    except Exception as e:
        click.secho(f"Error during search: {str(e)}", fg='red')


@click.command('search-cleanup')
@with_appcontext
def search_cleanup():
    """Clean up orphaned search index entries.
    
    Removes index entries for materials that no longer exist
    or have been unpublished.
    """
    click.echo("Scanning for orphaned search index entries...")
    
    orphaned_count = 0
    errors = []
    
    try:
        all_index_entries = SearchIndex.query.all()
        
        for entry in all_index_entries:
            material = Material.query.get(entry.material_id)
            
            # Remove if material doesn't exist or is unpublished
            if not material or not material.is_published:
                try:
                    SearchIndex.delete_index(entry.material_id)
                    orphaned_count += 1
                except Exception as e:
                    errors.append(f"Entry {entry.material_id}: {str(e)}")
        
        if orphaned_count > 0:
            click.secho(f"Removed {orphaned_count} orphaned entries", fg='green')
        else:
            click.secho("No orphaned entries found", fg='green')
        
        if errors:
            click.secho(f"\n{len(errors)} errors encountered:", fg='yellow')
            for error in errors:
                click.echo(f"  - {error}")
        
    except Exception as e:
        click.secho(f"Error during cleanup: {str(e)}", fg='red')


@click.command('search-reindex-material')
@click.option('--material-id', type=int, prompt='Material ID to reindex', 
              help='ID of the material to reindex')
@with_appcontext
def reindex_material(material_id):
    """Reindex a specific material."""
    material = Material.query.get(material_id)
    
    if not material:
        click.secho(f"Material {material_id} not found", fg='red')
        return
    
    if not material.is_published:
        click.secho(f"Material {material_id} is not published", fg='yellow')
        return
    
    try:
        SearchIndex.delete_index(material_id)
        search_index = SearchIndex.create_index(material)
        
        if search_index:
            click.secho(f"✓ Material {material_id} reindexed successfully", fg='green')
        else:
            click.secho(f"✗ Failed to reindex material {material_id}", fg='red')
    
    except Exception as e:
        click.secho(f"Error reindexing material: {str(e)}", fg='red')


def register_cli_commands(app):
    """Register Phase 3 CLI commands with Flask app.
    
    Args:
        app: Flask application instance
    """
    app.cli.add_command(rebuild_search_index)
    app.cli.add_command(search_stats)
    app.cli.add_command(search_test)
    app.cli.add_command(search_cleanup)
    app.cli.add_command(reindex_material)
