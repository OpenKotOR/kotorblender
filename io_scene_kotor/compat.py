# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

"""Blender API differences across the supported releases.

The supported Blender releases differ in how actions, mesh normals, lights and
materials are addressed. Every version check lives here, so the rest of the
add-on calls these helpers and the supported range stays readable in one file.
"""

import bpy

from bpy_extras import anim_utils

# Actions gained slots, one per animated ID sharing the action.
HAS_ACTION_SLOTS = bpy.app.version >= (4, 4)

# Action.fcurves reaches only the first slot from 4.4 on, and is gone in 5.0.
HAS_LEGACY_ACTION_FCURVES = bpy.app.version < (5, 0)

# Custom split normals needed auto smooth, and had to be recalculated by hand.
HAS_AUTO_SMOOTH = bpy.app.version < (4, 1)

# EEVEE Next dropped per-light contact shadows and per-material shadow modes.
HAS_LEGACY_EEVEE_SHADOWS = bpy.app.version < (4, 3)


def ensure_action_slot(action, id_type, name):
    """Return the slot of action for id_type and name, creating it if needed.

    Returns None before Blender 4.4, where actions have no slots.
    """
    if not HAS_ACTION_SLOTS:
        return None
    # action.slots is keyed by identifier, which prefixes the ID type
    # ("OBHead_g"), so a lookup by bare name never matches.
    for slot in action.slots:
        if slot.name_display == name and slot.target_id_type == id_type:
            return slot
    return action.slots.new(id_type=id_type, name=name)


def bound_action_slot(anim_data):
    """Return the slot anim_data is bound to, or None before Blender 4.4."""
    if not HAS_ACTION_SLOTS:
        return None
    return anim_data.action_slot


def bind_action_slot(anim_data, action_slot):
    """Bind anim_data to action_slot unless it is already bound to one."""
    if not HAS_ACTION_SLOTS or not action_slot:
        return
    if not anim_data.action_slot:
        anim_data.action_slot = action_slot


def ensure_fcurves(action, action_slot=None):
    """Return the F-curve collection to write into, creating it if needed."""
    if HAS_ACTION_SLOTS and action_slot:
        return _ensure_channelbag(action, action_slot).fcurves
    return action.fcurves


def find_fcurves(action, action_slot=None):
    """Return the F-curves to read, or None when this ID animates nothing.

    From Blender 4.4 an ID reads only the channels of the slot it is bound to:
    the legacy collection reaches the first slot, which may belong to another
    ID sharing the action.
    """
    if HAS_ACTION_SLOTS and action_slot:
        channelbag = anim_utils.action_get_channelbag_for_slot(action, action_slot)
        return channelbag.fcurves if channelbag else None
    if not HAS_LEGACY_ACTION_FCURVES:
        return None
    return action.fcurves


def clear_fcurves(action, action_slot=None):
    """Remove the F-curves action_slot owns, or all of them before slots."""
    ensure_fcurves(action, action_slot).clear()


def _ensure_channelbag(action, action_slot):
    """Return the channelbag holding action_slot's F-curves, creating it if needed.

    The anim_utils helper for this arrived in Blender 5.0; earlier versions get
    the same steps it takes, being the first layer, its first keyframe strip,
    then the slot's channelbag.
    """
    if hasattr(anim_utils, "action_ensure_channelbag_for_slot"):
        return anim_utils.action_ensure_channelbag_for_slot(action, action_slot)
    layer = action.layers[0] if action.layers else action.layers.new("Layer")
    strip = layer.strips[0] if layer.strips else layer.strips.new(type="KEYFRAME")
    return strip.channelbag(action_slot, ensure=True)


def set_custom_split_normals(mesh, loop_normals):
    """Give mesh per-loop custom normals."""
    mesh.normals_split_custom_set(loop_normals)
    if HAS_AUTO_SMOOTH:
        mesh.use_auto_smooth = True


def refresh_split_normals(mesh):
    """Make mesh.loops report split normals.

    Blender 4.1 computes them on demand; earlier versions need the call.
    """
    if HAS_AUTO_SMOOTH:
        mesh.calc_normals_split()


def set_contact_shadow(light, distance):
    """Enable contact shadows on light, where the render engine has them."""
    if HAS_LEGACY_EEVEE_SHADOWS:
        light.use_contact_shadow = True
        light.contact_shadow_distance = distance


def disable_material_shadows(material):
    """Stop material from casting shadows, where that is a material setting."""
    if HAS_LEGACY_EEVEE_SHADOWS:
        material.shadow_method = "NONE"
