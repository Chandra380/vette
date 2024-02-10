from flask import Flask, render_template, request
import os
import codecs

app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
resources_dir = os.path.join(project_dir, 'resources')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/file_view', methods=['GET'])
def file_view():
    filename = request.args.get('filename', 'file1.txt')
    start_line = int(request.args.get('start_line', 1))
    end_line = int(request.args.get('end_line', -1))

    try:
        file_path = os.path.join(resources_dir, filename)
        
        with codecs.open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            # Ensure start_line and end_line are within the valid range
            if start_line < 1:
                start_line = 1
            if end_line == -1:
                end_line = len(lines)
            elif end_line > len(lines):
                end_line = len(lines)
            

            print("Start line:", start_line)
            print("End line:", end_line)
            # Combine lines based on start_line and end_line
            content = ''.join(lines[start_line - 1:end_line])
            
            return render_template('file_view.html', content=content)
    except FileNotFoundError:
        return render_template('error.html', error='File not found')
    except ValueError:
        return render_template('error.html', error='Invalid line number')
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
