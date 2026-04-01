# Loop Logo Generator

A powerful web-based tool to create seamless looping GIF animations from static images. Features 24+ different animation types including 2D movements, 3D effects, distortions, and special effects.

## Features

- **24+ Animation Types** across 6 categories
- **Overlay Image Support** - Add static transparent images on top of all frames
- **Real-time Preview** with automatic regeneration
- **Customizable Parameters**:
  - Frame count (2-240)
  - Frame duration (10-5000ms)
  - Background color or transparent background
- **High-Quality Output** with optimized GIF compression
- **Modern UI** with clean, intuitive interface

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository:
```bash
git clone <repository-url>
cd loop-logo-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

Run the Flask application:
```bash
python app.py
```

The server will start at `http://localhost:5000`

### Creating Animations

1. **Select an Image**: Click the image upload button and choose your logo or image
2. **Add Overlay (Optional)**: Upload a transparent PNG to overlay on all frames
   - The overlay remains static while the base image animates
   - Perfect for adding borders, frames, or watermarks
   - Automatically resized to match the animation dimensions
3. **Choose Animation Type**: Select from 24+ animation types in the dropdown
4. **Customize Settings**:
   - Adjust frame count for smoothness
   - Set frame duration for speed
   - Choose background color or enable transparency
5. **Auto-Generate**: The GIF generates automatically as you adjust settings
6. **Download**: Click "Download GIF" to save your animation

### Overlay Feature

The overlay feature allows you to add a static image on top of your animation:

- **Use Cases**:
  - Add a static frame or border around animated content
  - Place a watermark that doesn't animate
  - Combine animated backgrounds with static foreground elements
  - Create picture-in-picture effects

- **Best Practices**:
  - Use transparent PNG files for best results
  - Ensure the overlay has transparency where you want the animation to show through
  - The overlay is automatically resized to match your animation dimensions
  - Remove the overlay by clearing the file input and regenerating

## Animation Types

### 2D Movements
- **Left/Right/Up/Down** - Classic directional scrolling
- **Diagonal Right/Left** - Smooth diagonal motion

### 3D Effects
- **3D Cube** - Rotating cube with perspective
- **3D Cylinder** - Cylindrical rotation with depth
- **3D Spin** - Horizontal axis rotation
- **3D Flip** - Vertical axis rotation

### Rotation & Spin
- **Rotate** - Pure 360° rotation
- **Spiral** - Rotation combined with zoom
- **Swirl** - Radial distortion effect
- **Twist** - Layered rotation
- **Pendulum** - Swinging motion

### Scale & Transform
- **Zoom Loop** - Zoom in with fade
- **Pulse** - Rhythmic scaling
- **Bounce** - Bouncing with squash & stretch
- **Elastic Bounce** - Bounce with overshoot
- **Slide + Scale** - Combined motion

### Distortion Effects
- **Wave** - Sine wave distortion
- **Shake** - Vibration effect
- **Glitch** - Digital glitch effect

### Fade Effects
- **Fade In/Out** - Smooth opacity transition

## Project Structure

```
loop-logo-generator/
├── app.py              # Flask application and API endpoints
├── animations.py       # Animation generation logic (24 types)
├── utils.py            # Helper functions (color parsing, etc.)
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── static/
│   ├── script.js      # Frontend JavaScript
│   └── style.css      # Styling
└── templates/
    └── index.html     # Main HTML page
```

## Configuration

### Frame Settings

- **Frames (2-240)**: Higher values create smoother animations but larger file sizes
  - Recommended: 24-60 frames for most animations
  
- **Frame Duration (10-5000ms)**: Time each frame is displayed
  - Recommended: 30-50ms for smooth motion
  - Higher values (100-200ms) for slower, more deliberate effects

### Background Options

- **Color Picker**: Choose any solid color background
- **Transparent Checkbox**: Enable for transparent background (useful for overlaying on websites)

## Technical Details

### Technologies Used

- **Backend**: Flask (Python web framework)
- **Image Processing**: Pillow (PIL)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3

### Overlay Implementation

Overlays are composited using PIL's `alpha_composite` function:
- Overlay image is loaded and converted to RGBA
- Resized to match the animation frame dimensions
- Applied to each frame after animation generation
- Maintains full transparency support

## Tips for Best Results

1. **Image Quality**: Use high-contrast images for better visibility
2. **Transparent PNGs**: Work great with transparent background option
3. **Square Images**: Maintain aspect ratio best in most animations
4. **Frame Count**: Balance between smoothness and file size
5. **Overlay Images**: Use transparent PNGs with clear areas for best overlay effects
6. **Animation Selection**: 
   - Use 3D effects for logos and icons
   - Use distortions for artistic effects
   - Use simple movements for backgrounds

## Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## License

This project is open source and available for personal and commercial use.

## Support

For issues, questions, or suggestions, please open an issue on the repository.