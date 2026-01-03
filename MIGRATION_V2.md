# Migrating to PicTex v2

## What Changed

PicTex v2 is a major rewrite focused on **CSS compliance** and **layout engine robustness**.

### Core Changes
1. **Layout Engine**: Migrated from custom Python layout to [Taffy](https://github.com/DioxusLabs/taffy) (via `stretchable` bindings). This provides battle-tested Flexbox layout.
2. **Positioning API**: Completely redesigned to match CSS positioning standards.
3. **Future API**: Method names will align with CSS terminology (e.g., `justify_content` instead of `horizontal_distribution`).

---

## Positioning API Migration

### Breaking Change: `absolute_position()`

**v1 Behavior** (deprecated):
```python
Text("Badge").absolute_position(10, 20)  # x=10, y=20 from parent top-left
```

**v2 Behavior** (CSS-style insets):
```python
# Position using CSS inset properties
Text("Badge").absolute_position(top=10, left=20)
Text("Footer").absolute_position(bottom=0, left=0, right=0)  # Stretch to bottom
```

### New Method: `place()`

For the old `absolute_position(x, y)` behavior, use `place()`:

```python
# v1
Text("Overlay").absolute_position("center", "center")

# v2 (same behavior)
Text("Overlay").place("center", "center")
```

`place()` supports:
- Keywords: `"left"`, `"center"`, `"right"`, `"top"`, `"bottom"`
- Pixels: `place(50, 100)`
- Percentages: `place("25%", "75%")`
- Offsets: `place("right", "top", x_offset=-10, y_offset=10)`

### New Method: `relative_position()`

Position an element relative to its normal flow position:

```python
Text("Nudged").relative_position(top=5, left=5)
```

### New Method: `translate()`

Apply post-layout transforms (useful for true centering):

```python
Text("Centered")
    .absolute_position(top="50%", left="50%")
    .translate(x="-50%", y="-50%")
```

---

## Layout API Renaming (CSS-Compliant)

Methods have been renamed to match standard CSS Flexbox terminology:

| Old Method (v1) | New Method (v2) | Applies To |
|:---|:---|:---|
| `horizontal_distribution()` | `justify_content()` | `Row` |
| `vertical_distribution()` | `justify_content()` | `Column` |
| `vertical_align()` | `align_items()` | `Row` |
| `horizontal_align()` | `align_items()` | `Column` |

**Migration:**
```python
# v1
Row(children).horizontal_distribution("center").vertical_align("center")
Column(children).vertical_distribution("space-between").horizontal_align("stretch")

# v2
Row(children).justify_content("center").align_items("center")
Column(children).justify_content("space-between").align_items("stretch")
```

**Supported values:**
- `justify_content`: `"start"`, `"center"`, `"end"`, `"space-between"`, `"space-around"`, `"space-evenly"`
- `align_items`: `"start"`, `"center"`, `"end"`, `"stretch"`

---

## Migration Checklist

- [ ] Replace `absolute_position(x, y)` with `place(x, y)` or `absolute_position(top=..., left=...)`
- [ ] Update `horizontal_distribution()`, `vertical_distribution()`, `vertical_align()`, `horizontal_align()` to `justify_content()` and `align_items()`
- [ ] Test layouts with the new engine (run your test suite)

---

## New Flex Properties

v2.0 adds full CSS Flexbox control:

### Item-Level Control

**`flex_grow(value: float)`** - Control growth behavior:
```python
Row(
    Text("Fixed").size(width=100),
    Text("Grows x1").flex_grow(1),  # Gets 1 share of remaining space
    Text("Grows x2").flex_grow(2)   # Gets 2 shares (twice as much)
)
```

**`flex_shrink(value: float)`** - Control shrink behavior:
```python
Row(
    Text("Don't shrink me").flex_shrink(0),
    Text("Can shrink").flex_shrink(1)
)
```

**`align_self(alignment)`** - Override container alignment:
```python
Row(
    Text("A"),
    Text("B").align_self('end'),  # Overrides the Row's align_items
    Text("C")
).align_items('start')
```

### Container-Level Control

**`flex_wrap(mode)`** - Enable multi-line layouts:
```python
Row(
    *[Text(f"Item {i}").size(width=100) for i in range(20)]
).flex_wrap('wrap').size(width=500)  # Creates a responsive grid
```

Values: `'nowrap'` (default), `'wrap'`, `'wrap-reverse'`

---

## Migration Checklist

- Check the [CHANGELOG](CHANGELOG.md) for detailed version history
- Review [css_compliance_analysis.md](css_compliance_analysis.md) for the full technical breakdown
- Open an issue on GitHub if you encounter migration problems
