# Migration Guide: v1.x to v2.0

This guide covers breaking changes introduced in PicTex v2.0 and provides migration paths for existing code.

## Overview

PicTex v2.0 is a major release focused on CSS compliance and layout engine robustness. The update includes:

- **Layout engine**: Migrated to Taffy (via `stretchable` bindings) for production-grade Flexbox layout
- **API standardization**: Method names now align with CSS Flexbox terminology
- **Positioning system**: Redesigned to follow CSS positioning standards

---

## Breaking Changes

### 1. Positioning API

#### `absolute_position()` signature changed

The `absolute_position()` method now uses CSS-style inset properties instead of positional arguments.

**Before (v1.x):**
```python
Text("Badge").absolute_position(10, 20)  # x=10, y=20
```

**After (v2.0):**
```python
# Option A: Use CSS insets
Text("Badge").absolute_position(top=20, left=10)

# Option B: Use place() for anchor-based positioning
Text("Badge").place(10, 20)
```

The new `place()` method provides the same anchor-based positioning as the old API:
- Supports keywords: `"left"`, `"center"`, `"right"`, `"top"`, `"bottom"`
- Supports pixels: `place(50, 100)`
- Supports percentages: `place("25%", "75%")`
- Supports offsets: `place("right", "top", x_offset=-10, y_offset=10)`

---

### 2. Layout Method Renaming

Container layout methods have been renamed to match CSS Flexbox terminology.

| v1.x Method | v2.0 Method | Container |
|-------------|-------------|-----------|
| `horizontal_distribution()` | `justify_content()` | `Row` |
| `vertical_distribution()` | `justify_content()` | `Column` |
| `vertical_align()` | `align_items()` | `Row` |
| `horizontal_align()` | `align_items()` | `Column` |

**Before (v1.x):**
```python
Row(children).horizontal_distribution("center").vertical_align("center")
Column(children).vertical_distribution("space-between").horizontal_align("stretch")
```

**After (v2.0):**
```python
Row(children).justify_content("center").align_items("center")
Column(children).justify_content("space-between").align_items("stretch")
```

#### Supported values

- **`justify_content`**: `"start"`, `"center"`, `"end"`, `"space-between"`, `"space-around"`, `"space-evenly"`
- **`align_items`**: `"start"`, `"center"`, `"end"`, `"stretch"`

**Note**: Legacy value aliases (e.g., `"left"`, `"right"`, `"top"`, `"bottom"`) are not supported. Use standard CSS values.

---

### 3. Removal of `fill-available` Size Mode

The `'fill-available'` size mode has been removed in favor of the explicit `flex_grow()` method for CSS compliance.

**Before (v1.x):**
```python
Text("Flexible").size(width='fill-available')
Row(children).size(height='fill-available')
```

**After (v2.0):**
```python
Text("Flexible").flex_grow(1)
Row(children).flex_grow(1)
```

**Rationale**: In CSS, "filling available space" is a flex behavior (`flex-grow`), not a size value. This change makes the API more explicit and aligns with CSS Flexbox standards.

---

## Additional Methods

v2.0 introduces new positioning methods:

### `relative_position()`

Position an element relative to its normal flow position:
```python
Text("Nudged").relative_position(top=5, left=5)
```

### `place()`

Anchor-based positioning (replaces old `absolute_position(x, y)` behavior):
```python
Text("Overlay").place("center", "center")
```

### `translate()`

Apply post-layout transforms:
```python
Text("Centered")
    .absolute_position(top="50%", left="50%")
    .translate(x="-50%", y="-50%")
```

---

## Migration Checklist

- [ ] Replace `absolute_position(x, y)` calls with either:
  - `place(x, y)` for anchor-based positioning, or
  - `absolute_position(top=y, left=x)` for CSS-style positioning
- [ ] Rename layout methods:
  - `horizontal_distribution()` → `justify_content()`
  - `vertical_distribution()` → `justify_content()`
  - `vertical_align()` → `align_items()`
  - `horizontal_align()` → `align_items()`
- [ ] Replace `size(width='fill-available')` and `size(height='fill-available')` with `flex_grow(1)`
- [ ] Update alignment values to use CSS standard values (`"start"`, `"end"`, etc.)
- [ ] Run your test suite to verify layouts render correctly with the new engine

---

## New Features

For information about new features in v2.0 (such as `flex_grow`, `flex_shrink`, `aspect_ratio`, and size constraints), see the [CHANGELOG](CHANGELOG.md).

---

## Support

If you encounter issues during migration:
- Review the [CHANGELOG](CHANGELOG.md) for detailed version history
- Check existing [GitHub issues](https://github.com/francozanardi/pictex/issues)
- Open a new issue if you find a bug or need help
