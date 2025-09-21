from flask import Flask, render_template, request, redirect, url_for
import pyfiglet

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        font = request.form.get('font', 'standard')
        
        # Validate input
        if not text:
            return render_template('index.html', 
                                 ascii_art='', 
                                 error_message="Please enter some text to convert.",
                                 text_value=text,
                                 font_value=font)
        
        try:
            # Try to create the figlet with the specified font
            fig = pyfiglet.Figlet(font=font)
            ascii_art = fig.renderText(text)
            return render_template('index.html', 
                                 ascii_art=ascii_art, 
                                 error_message='',
                                 text_value=text,
                                 font_value=font)
        except pyfiglet.FontNotFound:
            # Handle invalid font gracefully
            error_message = f"Font '{font}' not found. Using standard font instead."
            fig = pyfiglet.Figlet(font='standard')
            ascii_art = fig.renderText(text)
            return render_template('index.html', 
                                 ascii_art=ascii_art, 
                                 error_message=error_message,
                                 text_value=text,
                                 font_value=font)
        except Exception as e:
            # Handle any other unexpected errors
            error_message = "An error occurred while generating ASCII art. Please try again."
            print(f"Unexpected error: {e}")  # Log for debugging
            return render_template('index.html', 
                                 ascii_art='', 
                                 error_message=error_message,
                                 text_value=text,
                                 font_value=font)
    
    # GET request - render clean form with no output
    return render_template('index.html', 
                         ascii_art='', 
                         error_message='',
                         text_value='',
                         font_value='block')

@app.route('/clear')
def clear():
    """Route to completely clear and redirect to fresh page"""
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
