from flask import Blueprint, jsonify, request
from src.models.note import Note, db

note_bp = Blueprint('note', __name__)

#An endpoint to return the number of notes
@note_bp.route('/notes/count', methods=['GET']) 
def get_notes_count():
    """Get the total count of notes"""
    count = Note.query.count()
    return jsonify({'count': count})   



@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes, ordered by most recently updated"""
    notes = Note.query.order_by(Note.updated_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@note_bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content are required'}), 400
        
        from datetime import datetime, date, time
        tags = data.get('tags', [])
        tags_str = ','.join(tags) if isinstance(tags, list) else (tags or '')
        event_date_str = data.get('event_date')
        event_time_str = data.get('event_time')

        event_date = None
        event_time = None
        if event_date_str:
            try:
                event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
            except Exception:
                event_date = None
        if event_time_str:
            try:
                event_time = datetime.strptime(event_time_str, '%H:%M').time()
            except Exception:
                event_time = None

        note = Note(
            title=data['title'],
            content=data['content'],
            tags=tags_str,
            event_date=event_date,
            event_time=event_time
        )
        db.session.add(note)
        db.session.commit()
        return jsonify(note.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

@note_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        from datetime import datetime, date, time
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        tags = data.get('tags', None)
        if tags is not None:
            note.tags = ','.join(tags) if isinstance(tags, list) else (tags or '')
        event_date_str = data.get('event_date', None)
        if event_date_str is not None:
            try:
                note.event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date() if event_date_str else None
            except Exception:
                note.event_date = None
        event_time_str = data.get('event_time', None)
        if event_time_str is not None:
            try:
                note.event_time = datetime.strptime(event_time_str, '%H:%M').time() if event_time_str else None
            except Exception:
                note.event_time = None
        db.session.commit()
        return jsonify(note.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    """Search notes by title or content"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    notes = Note.query.filter(
        (Note.title.contains(query)) | (Note.content.contains(query))
    ).order_by(Note.updated_at.desc()).all()
    
    return jsonify([note.to_dict() for note in notes])


# Translation endpoint: POST /api/notes/<id>/translate
@note_bp.route('/notes/<int:note_id>/translate', methods=['POST'])
def translate_note(note_id):
    """Translate a note's title and content to a target language (ephemeral, no DB change)"""
    note = Note.query.get_or_404(note_id)
    data = request.json or {}
    target_language = data.get('target_language')
    if not target_language:
        return jsonify({'error': 'target_language required'}), 400
    from src.llm import translate_to_language
    try:
        translated_title = translate_to_language(note.title, target_language)
        translated_content = translate_to_language(note.content, target_language)
        return jsonify({
            'note_id': note.id,
            'target_language': target_language,
            'translated_title': translated_title,
            'translated_content': translated_content
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/generate', methods=['POST'])
def generate_note():
    """Generate a note using AI from natural language input"""
    try:
        data = request.json
        if not data or 'input_text' not in data:
            return jsonify({'error': 'Input text is required'}), 400
        
        from src.llm import generate_note_from_text
        generated = generate_note_from_text(data['input_text'])
        
        return jsonify(generated), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

