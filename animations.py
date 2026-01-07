"""Animation generation logic for the loop logo generator."""

import math
from typing import List, Tuple

from PIL import Image


# All supported animation types
VALID_ANIMATION_TYPES = {
    "left", "right", "up", "down", 
    "cube", "cylinder", "zoom", "spin", "flip", 
    "wave", "spiral", "rotate", "bounce", "twist",
    "diagonal-right", "diagonal-left", "pulse", "shake", 
    "glitch", "swirl", "pendulum", "elastic", "slide-scale", "fade"
}


def build_frames(
    source: Image.Image, 
    animation_type: str, 
    frames: int, 
    bg_color: Tuple[int, int, int, int]
) -> List[Image.Image]:
    """
    Generate animation frames based on the specified animation type.
    
    Args:
        source: The source image to animate
        animation_type: Type of animation to apply
        frames: Number of frames to generate
        bg_color: Background color as RGBA tuple
    
    Returns:
        List of PIL Image objects representing the animation frames
    """
    width, height = source.size
    results: List[Image.Image] = []

    if animation_type in {"left", "right", "up", "down"}:
        is_horizontal = animation_type in {"left", "right"}
        travel = width if is_horizontal else height
        for idx in range(frames):
            progress = idx / frames
            shift = int(round(progress * travel))
            frame = Image.new("RGBA", (width, height), bg_color)
            if animation_type == "left":
                offsets = [(-shift, 0), (width - shift, 0)]
            elif animation_type == "right":
                offsets = [(shift, 0), (shift - width, 0)]
            elif animation_type == "up":
                offsets = [(0, -shift), (0, height - shift)]
            else:  # down
                offsets = [(0, shift), (0, shift - height)]
            for ox, oy in offsets:
                frame.paste(source, (ox, oy), source)
            results.append(frame)

    elif animation_type == "cube":
        # Simulate a 360-degree rotation of a cube with perspective
        source_flipped = source.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        faces = [source, source_flipped, source, source_flipped]
        
        for idx in range(frames):
            progress = idx / frames
            total_angle = progress * 2 * math.pi
            
            quadrant = int((total_angle / (math.pi / 2)) % 4)
            angle = total_angle % (math.pi / 2)
            
            frame = Image.new("RGBA", (width, height), bg_color)
            
            # Face A (currently in front, rotating away)
            cos_a = math.cos(angle)
            w1 = int(width * cos_a)
            h1 = int(height * (0.85 + 0.15 * cos_a))
            
            if w1 > 2:
                face_a = faces[quadrant].resize((w1, h1), Image.Resampling.LANCZOS)
                y_offset = (height - h1) // 2
                frame.paste(face_a, (width // 2 - w1, y_offset), face_a)
            
            # Face B (coming from the side to front)
            sin_a = math.sin(angle)
            w2 = int(width * sin_a)
            h2 = int(height * (0.85 + 0.15 * sin_a))
            
            if w2 > 2:
                face_b = faces[(quadrant + 1) % 4].resize((w2, h2), Image.Resampling.LANCZOS)
                y_offset = (height - h2) // 2
                frame.paste(face_b, (width // 2, y_offset), face_b)
            
            results.append(frame)

    elif animation_type == "cylinder":
        # Zoom out to see the full cylinder
        zoom_factor = 0.7
        canvas_w = int(width / zoom_factor)
        canvas_h = int(height / zoom_factor)
        
        for idx in range(frames):
            progress = idx / frames
            canvas = Image.new("RGBA", (canvas_w, canvas_h), bg_color)
            
            phi = progress * 2 * math.pi
            
            num_slices = 120
            
            for s in range(num_slices):
                theta = (s / num_slices - 0.5) * math.pi
                
                # Horizontal projection
                px = int((math.sin(theta) * 0.5 + 0.5) * canvas_w)
                theta_next = ((s + 1) / num_slices - 0.5) * math.pi
                px_next = int((math.sin(theta_next) * 0.5 + 0.5) * canvas_w)
                pw = max(1, px_next - px)
                
                # Source mapping
                alpha = (phi + theta) % (2 * math.pi)
                sx = int((alpha / (2 * math.pi)) * width) % width
                sw = max(1, int((1.0 / num_slices) * 0.5 * width))
                
                if sx + sw <= width:
                    img_slice = source.crop((sx, 0, sx + sw, height))
                else:
                    img_slice = Image.new("RGBA", (sw, height))
                    part1 = source.crop((sx, 0, width, height))
                    part2 = source.crop((0, 0, sw - (width - sx), height))
                    img_slice.paste(part1, (0, 0))
                    img_slice.paste(part2, (width - sx, 0))
                
                # Vertical scaling for cylindrical perspective
                cos_theta = math.cos(theta)
                h_scale = 0.92 + (0.08 * abs(cos_theta))
                ph = int(canvas_h * h_scale)
                
                img_slice = img_slice.resize((pw, ph), Image.Resampling.LANCZOS)
                
                py = (canvas_h - ph) // 2
                canvas.paste(img_slice, (px, py), img_slice)
            
            # Scale back to original size
            frame = canvas.resize((width, height), Image.Resampling.LANCZOS)
            results.append(frame)

    elif animation_type == "zoom":
        for idx in range(frames):
            progress = idx / frames
            scale = 1.0 + progress
            new_w, new_h = int(width * scale), int(height * scale)
            zoomed = source.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # Create a copy with alpha for fading
            faded = zoomed.copy()
            alpha_multiplier = 1.0 - (progress ** 2)
            mask = faded.split()[3].point(lambda p: int(p * alpha_multiplier))
            faded.putalpha(mask)
            
            frame = Image.new("RGBA", (width, height), bg_color)
            frame.paste(faded, ((width - new_w) // 2, (height - new_h) // 2), faded)
            results.append(frame)

    elif animation_type == "spin":
        # 360 degree spin around Y axis with perspective
        for idx in range(frames):
            progress = idx / frames
            angle = progress * 2 * math.pi
            frame = Image.new("RGBA", (width, height), bg_color)
            
            w_factor = math.cos(angle)
            curr_w = int(abs(width * w_factor))
            h_factor = 0.90 + (0.10 * abs(w_factor))
            curr_h = int(height * h_factor)
            
            if curr_w > 2:
                side = source
                if w_factor < 0:
                    side = source.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                
                spun = side.resize((curr_w, curr_h), Image.Resampling.LANCZOS)
                
                x_offset = (width - curr_w) // 2
                y_offset = (height - curr_h) // 2
                frame.paste(spun, (x_offset, y_offset), spun)
            
            results.append(frame)

    elif animation_type == "flip":
        # Card flip - rotating around X axis
        source_flipped = source.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        
        for idx in range(frames):
            progress = idx / frames
            angle = progress * 2 * math.pi
            frame = Image.new("RGBA", (width, height), bg_color)
            
            h_factor = math.cos(angle)
            curr_h = int(abs(height * h_factor))
            w_factor = 0.92 + (0.08 * abs(h_factor))
            curr_w = int(width * w_factor)
            
            if curr_h > 2:
                side = source
                if h_factor < 0:
                    side = source_flipped
                
                flipped = side.resize((curr_w, curr_h), Image.Resampling.LANCZOS)
                
                x_offset = (width - curr_w) // 2
                y_offset = (height - curr_h) // 2
                frame.paste(flipped, (x_offset, y_offset), flipped)
            
            results.append(frame)

    elif animation_type == "wave":
        # Wave effect - sine wave distortion
        for idx in range(frames):
            progress = idx / frames
            frame = Image.new("RGBA", (width, height), bg_color)
            
            wave_phase = progress * 2 * math.pi
            amplitude = width * 0.05
            frequency = 3
            
            for y in range(height):
                offset = int(amplitude * math.sin(wave_phase + (y / height) * frequency * 2 * math.pi))
                
                if offset >= 0:
                    if offset < width:
                        row = source.crop((0, y, width - offset, y + 1))
                        frame.paste(row, (offset, y))
                        wrap = source.crop((width - offset, y, width, y + 1))
                        frame.paste(wrap, (0, y))
                else:
                    offset = abs(offset)
                    if offset < width:
                        row = source.crop((offset, y, width, y + 1))
                        frame.paste(row, (0, y))
                        wrap = source.crop((0, y, offset, y + 1))
                        frame.paste(wrap, (width - offset, y))
            
            results.append(frame)

    elif animation_type == "spiral":
        # Spiral - rotation + zoom combined
        for idx in range(frames):
            progress = idx / frames
            frame = Image.new("RGBA", (width, height), bg_color)
            
            angle_deg = progress * 360
            scale = 1.0 + (math.sin(progress * 2 * math.pi) * 0.3)
            
            new_w = int(width * scale)
            new_h = int(height * scale)
            
            rotated = source.rotate(-angle_deg, resample=Image.Resampling.BICUBIC, expand=False)
            scaled = rotated.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            alpha_multiplier = 0.6 + (scale * 0.4)
            if alpha_multiplier < 1.0:
                r, g, b, a = scaled.split()
                a = a.point(lambda p: int(p * alpha_multiplier))
                scaled = Image.merge("RGBA", (r, g, b, a))
            
            x_offset = (width - new_w) // 2
            y_offset = (height - new_h) // 2
            frame.paste(scaled, (x_offset, y_offset), scaled)
            
            results.append(frame)

    elif animation_type == "rotate":
        # Pure rotation - 360 degree spin without zoom
        for idx in range(frames):
            progress = idx / frames
            frame = Image.new("RGBA", (width, height), bg_color)
            
            angle_deg = progress * 360
            rotated = source.rotate(-angle_deg, resample=Image.Resampling.BICUBIC, expand=False)
            
            frame.paste(rotated, (0, 0), rotated)
            
            results.append(frame)

    elif animation_type == "bounce":
        # Bounce effect - vertical bouncing with squash and stretch
        for idx in range(frames):
            progress = idx / frames
            frame = Image.new("RGBA", (width, height), bg_color)
            
            bounce = abs(math.sin(progress * 2 * math.pi))
            
            max_height_offset = int(height * 0.3)
            y_offset = int(max_height_offset * (1 - bounce))
            
            stretch_factor = 1.0 + (bounce * 0.2)
            squash_factor = 1.0 - (bounce * 0.1)
            
            curr_h = int(height * stretch_factor)
            curr_w = int(width * squash_factor)
            
            bounced = source.resize((curr_w, curr_h), Image.Resampling.LANCZOS)
            
            x_offset = (width - curr_w) // 2
            y_final = y_offset
            
            frame.paste(bounced, (x_offset, y_final), bounced)
            
            results.append(frame)

    elif animation_type == "twist":
        # Twist effect - rotating slices at different speeds
        for idx in range(frames):
            progress = idx / frames
            frame = Image.new("RGBA", (width, height), bg_color)
            
            num_slices = 20
            slice_height = height // num_slices
            
            for s in range(num_slices):
                y_start = s * slice_height
                y_end = min(y_start + slice_height, height)
                
                twist_amount = (s / num_slices) * progress * 360
                
                slice_img = source.crop((0, y_start, width, y_end))
                rotated_slice = slice_img.rotate(
                    -twist_amount, 
                    resample=Image.Resampling.BICUBIC,
                    expand=False
                )
                
                scale = 0.95 + (0.05 * math.cos((s / num_slices + progress) * 2 * math.pi))
                new_w = int(width * scale)
                slice_h = y_end - y_start
                new_h = int(slice_h * scale)
                
                if new_w > 0 and new_h > 0:
                    rotated_slice = rotated_slice.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    x_offset = (width - new_w) // 2
                    y_offset = y_start + (slice_h - new_h) // 2
                    frame.paste(rotated_slice, (x_offset, y_offset), rotated_slice)
            
            results.append(frame)

    elif animation_type == "diagonal-right":
        # Diagonal slide from top-left to bottom-right
        travel = int(math.sqrt(width**2 + height**2))
        
        for idx in range(frames):
            progress = idx / frames
            shift = int(progress * travel)
            frame = Image.new("RGBA", (width, height), bg_color)
            
            x_shift = int((shift / travel) * width)
            y_shift = int((shift / travel) * height)
            
            offsets = [
                (-x_shift, -y_shift),
                (width - x_shift, -y_shift),
                (-x_shift, height - y_shift),
                (width - x_shift, height - y_shift)
            ]
            
            for ox, oy in offsets:
                frame.paste(source, (ox, oy), source)
            
            results.append(frame)

    elif animation_type == "diagonal-left":
        # Diagonal slide from top-right to bottom-left
        travel = int(math.sqrt(width**2 + height**2))
        
        for idx in range(frames):
            progress = idx / frames
            shift = int(progress * travel)
            frame = Image.new("RGBA", (width, height), bg_color)
            
            x_shift = int((shift / travel) * width)
            y_shift = int((shift / travel) * height)
            
            offsets = [
                (x_shift, -y_shift),
                (x_shift - width, -y_shift),
                (x_shift, height - y_shift),
                (x_shift - width, height - y_shift)
            ]
            
            for ox, oy in offsets:
                frame.paste(source, (ox, oy), source)
            
            results.append(frame)

    elif animation_type == "pulse":
        # Pulsing scale effect
        for idx in range(frames):
            progress = idx / frames
            scale = 1.0 + (0.3 * math.sin(progress * 4 * math.pi))
            
            new_w = int(width * scale)
            new_h = int(height * scale)
            
            pulsed = source.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            frame = Image.new("RGBA", (width, height), bg_color)
            x_offset = (width - new_w) // 2
            y_offset = (height - new_h) // 2
            frame.paste(pulsed, (x_offset, y_offset), pulsed)
            
            results.append(frame)

    elif animation_type == "shake":
        # Shake/vibrate effect
        for idx in range(frames):
            progress = idx / frames
            frame = Image.new("RGBA", (width, height), bg_color)
            
            x_shake = int(10 * math.sin(progress * 30 * math.pi))
            y_shake = int(8 * math.sin(progress * 25 * math.pi))
            
            frame.paste(source, (x_shake, y_shake), source)
            
            results.append(frame)

    elif animation_type == "glitch":
        # Glitch effect with horizontal slices
        for idx in range(frames):
            progress = idx / frames
            frame = Image.new("RGBA", (width, height), bg_color)
            
            num_glitch_slices = 15
            slice_h = height // num_glitch_slices
            
            for s in range(num_glitch_slices):
                y = s * slice_h
                y_end = min(y + slice_h, height)
                
                if (s + int(progress * 10)) % 3 == 0:
                    shift = int(20 * math.sin(progress * 10 * math.pi + s))
                    
                    slice_img = source.crop((0, y, width, y_end))
                    if shift > 0:
                        left_part = slice_img.crop((width - shift, 0, width, slice_h))
                        right_part = slice_img.crop((0, 0, width - shift, slice_h))
                        wrapped = Image.new("RGBA", (width, slice_h))
                        wrapped.paste(left_part, (0, 0))
                        wrapped.paste(right_part, (shift, 0))
                        frame.paste(wrapped, (0, y), wrapped)
                    else:
                        frame.paste(slice_img, (shift, y), slice_img)
                else:
                    slice_img = source.crop((0, y, width, y_end))
                    frame.paste(slice_img, (0, y), slice_img)
            
            results.append(frame)

    elif animation_type == "swirl":
        # Swirl effect - different from spiral
        for idx in range(frames):
            progress = idx / frames
            frame = Image.new("RGBA", (width, height), bg_color)
            
            center_x, center_y = width // 2, height // 2
            max_radius = math.sqrt(center_x**2 + center_y**2)
            
            for y in range(height):
                for x in range(width):
                    dx = x - center_x
                    dy = y - center_y
                    distance = math.sqrt(dx**2 + dy**2)
                    
                    if distance > 0:
                        rotation = (distance / max_radius) * progress * 2 * math.pi
                        
                        angle = math.atan2(dy, dx) + rotation
                        new_x = int(center_x + distance * math.cos(angle))
                        new_y = int(center_y + distance * math.sin(angle))
                        
                        src_x = new_x % width
                        src_y = new_y % height
                        
                        pixel = source.getpixel((src_x, src_y))
                        frame.putpixel((x, y), pixel)
            
            results.append(frame)

    elif animation_type == "pendulum":
        # Pendulum swing effect
        for idx in range(frames):
            progress = idx / frames
            frame = Image.new("RGBA", (width, height), bg_color)
            
            max_angle = 30
            angle = max_angle * math.sin(progress * 2 * math.pi)
            
            rotated = source.rotate(angle, resample=Image.Resampling.BICUBIC, expand=False)
            
            x_offset = int(20 * math.sin(progress * 2 * math.pi))
            
            frame.paste(rotated, (x_offset, 0), rotated)
            
            results.append(frame)

    elif animation_type == "elastic":
        # Elastic bounce with overshoot
        for idx in range(frames):
            progress = idx / frames
            frame = Image.new("RGBA", (width, height), bg_color)
            
            t = progress * 2
            if t < 1:
                bounce_val = t * t * ((2.5 + 1) * t - 2.5)
            else:
                t -= 2
                bounce_val = 1 + t * t * ((2.5 + 1) * t + 2.5)
            
            bounce_val = max(0, min(1, bounce_val))
            
            max_y = int(height * 0.4)
            y_pos = int(max_y * (1 - bounce_val))
            
            h_scale = 0.8 + (bounce_val * 0.4)
            w_scale = 1.2 - (bounce_val * 0.4)
            
            new_w = int(width * w_scale)
            new_h = int(height * h_scale)
            
            elastic = source.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            x_offset = (width - new_w) // 2
            frame.paste(elastic, (x_offset, y_pos), elastic)
            
            results.append(frame)

    elif animation_type == "slide-scale":
        # Slide left while scaling down then up
        for idx in range(frames):
            progress = idx / frames
            frame = Image.new("RGBA", (width, height), bg_color)
            
            x_offset = -int(progress * width)
            
            scale = 0.7 + (0.6 * abs(math.sin(progress * math.pi)))
            new_w = int(width * scale)
            new_h = int(height * scale)
            
            scaled = source.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            y_offset = (height - new_h) // 2
            
            frame.paste(scaled, (x_offset, y_offset), scaled)
            frame.paste(scaled, (x_offset + width, y_offset), scaled)
            
            results.append(frame)

    elif animation_type == "fade":
        # Fade in and out
        for idx in range(frames):
            progress = idx / frames
            frame = Image.new("RGBA", (width, height), bg_color)
            
            opacity = abs(math.sin(progress * 2 * math.pi))
            
            faded = source.copy()
            r, g, b, a = faded.split()
            a = a.point(lambda p: int(p * opacity))
            faded = Image.merge("RGBA", (r, g, b, a))
            
            frame.paste(faded, (0, 0), faded)
            
            results.append(frame)

    return results

