from database import SessionLocal, engine
from models import Base, Task
from sqlalchemy import text

#Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        db.query(Task).delete()
        db.execute(text("DELETE FROM task_dependencies"))
        db.commit()

        all_tasks = []

        # ------------------ ORIGINS: BASIC TOOLS ------------------
        collect_shovel = Task(title="Collect shovel", description="Locations : \n - In hallway where door unlock to gen 3 is\n - Immediately after spawning to the right of Maxis Brain, leaning on wall\n*NOTE* : Needed to dig up Ice Staff parts during snow weather", goal="Origins")

        # ------------------ ORIGINS: ZOMBIE SHIELD ------------------
        s_handle = Task(title="Collect shield part (Handle)", description="Locations (Gen 2 trenches) : \n - Inside wheelbarrow in the room on the right directly after exiting spawn room\n - End of gen 2 trenches in wheelbarrow\n - Top of Tank Station near large pipe", goal="Origins")
        s_visor = Task(title="Collect shield part (Visor)", description="Locations (Gen 3 trenches) : \n - Bottom of Fire Tunnel directly outside spawn on left\n - Wheelbarrow in room opposite of Fire Tunnel\n - Underneath bridge next to Gen 3, part is next to crate", goal="Origins")
        s_frame = Task(title="Collect shield part (Frame)", description="Locations (No Man's Land) : \n - Inside giant's right footprint near Gen 4\n - Inside giant's right footprint near Gen 5\n - Inside giant's right footprint next to the Mound", goal="Origins")
        build_shield = Task(title="Build Shield at worbench", description="Workbenches are located at most major locations, wind tunnel workbench is the most effective", goal="Origins")

        # ------------------ ORIGINS: GENERATORS ------------------
        gen1 = Task(title="Power on Gen 1", description="Capture Generator 1 (Spawn area)", goal="Origins")
        gen2 = Task(title="Power on Gen 2", description="Capture Generator 2 (Tank Station)", goal="Origins")
        gen3 = Task(title="Power on Gen 3", description="Capture Generator 3 (Near Speed-cola)", goal="Origins")
        gen4 = Task(title="Power on Gen 4", description="Capture Generator 4 (Next to Juggernog)", goal="Origins")
        gen5 = Task(title="Power on Gen 5", description="Capture Generator 5 (Next to Stamin-Up)", goal="Origins")
        gen6 = Task(title="Power on Gen 6", description="Capture Generator 6 (Back of Church)", goal="Origins")

        # ------------------ ORIGINS: MAXIS DRONE ------------------
        d_rotor = Task(title="Collect Maxis Drone Rotor", description="Locations : \n - Top of mound in a wheelbarrow\n - Left of gramophone table at the middle level of excavation\n - Bottom level of excavation scaffolding", goal="Origins")
        d_brain = Task(title="Collect Maxis Drone Brain", description="On bench as soon as you spawn (Gen 1)", goal="Origins")
        d_frame = Task(title="Collect Maxis Drone Frame", description="Locations : \n - Tank exit path out of church\n - Tank return path\n - Bottom of ice tunnel", goal="Origins")
        build_drone = Task(title="Build Maxis Drone", description="Use the collected parts at any workbench.", goal="Origins")

        # ------------------ ORIGINS: WHITE RECORD ------------------
        collect_white_record = Task(title="Collect Blank Disk (White Record)", description="Locations (Mound Area) : \n - Behind the excavation sign at the front of mound (Mound side that faces Gen 1/2/3)\n - Behind the mound on a wall near crates (Around church entrance path)\n - In a wheelbarrow at the very top of the mound", goal="Origins")

        # ------------------ ORIGINS: EXCAVATION ACCESS / GRAMAPHONE ------------------
        collect_gramophone = Task(title="Collect gramophone", description="Location (Inside Mound/Excavation) : \n - On the floor in the middle level of excavation, next to bench", goal="Origins")
        place_gramophone = Task(title="Immediately place gramophone in Mound to unlock lower level of excavation", description="Place it on the bench that it was lying next to in excavation to unlock lower level excavation (Where the staffs will be built)", goal="Origins")
        retrieve_gramophone = Task(title="Pick gramophone back up from middle level of excavation", description="Once lower level of excavation is open, pick gramaphone back up. You will need this to enter the crazy place", goal="Origins")

        # ------------------ ORIGINS: ICE STAFF ------------------
        ice_disk = Task(title="Collect Blue Disk (Ice Record)", description="Locations (Gen 2 Tank Station):\n• Desk near the entrance\n• Shelf on the left after entering\n• Shelf in the back near the exit", goal="Origins")
        ice_p_spawn = Task(title="Collect Ice Staff part (Spawn area)", description="Dig up dig sites during a SNOW round in the starting area (Gen 2 trenches / Gen 3 trenches). \n *NOTE* The staff piece will never come from first dig in a given area, multiple digs required", goal="Origins")
        ice_p_middle = Task(title="Collect Ice Staff part (No Man's Land)", description="Dig up dig sites during a SNOW round in no mans land (Gen 4 / Gen 5). \n *NOTE* The staff piece will never come from first dig in a given area, multiple digs required", goal="Origins")
        ice_p_church = Task(title="Collect Ice Staff part (Church area)", description="Dig up dig sites during a SNOW round in the Church or Gen 6 area. \n *NOTE* The staff piece will never come from first dig in a given area, multiple digs required", goal="Origins")
        ice_portal = Task(title="Enter Ice Portal & Retrieve Gem", description="Place gramophone at Gen 6 tunnel. Retrieve the Blue Gem from ice pedestal and exit. *NOTE* You may have left gramaphone somewhere else (Go pick it up)", goal="Origins")
        build_ice = Task(title="Build Ice Staff", description="Build at the Blue Altar in the lower excavation.", goal="Origins")
        ice_puzzle = Task(title="Solve Ice Puzzle (Crazy Place)", description="Match the ceiling tile symbols to the blue tablet icons. (IN PROGRESS)", goal="Origins")
        ice_graves = Task(title="Freeze & Shoot 3 Gravestones", description="Locations : \n - Near right giant footprint (Gen 4)\n - Near right giant footprint (Mound)\n - Tank path outside Tank Station (Up the mud path)", goal="Origins")
        ice_orb = Task(title="Align Gems & Shoot Blue Orb", description="Rotate all the rings in lower excavation to BLUE using the glowing levers in lower excavation, then shoot the blue orb at the bottom with ice staff.", goal="Origins")
        ice_altar = Task(title="Place Staff in Ice Altar", description="Return to the Crazy Place and place the ice staff in the ice pedestal.", goal="Origins")
        ice_portal_exit = Task(title="(ICE) Exit crazy place *READ DESC*", description="At this point you can either :\n A. Leave the crazy place and upgrade all the staffs at the same time later. \n B. Upgrade the ice staff by getting kills in the crazy place while it is in the altar", goal="Origins")
        retrieve_gram_ice = Task(title="Pick up gramophone (ICE tunnel) (Gen 6)", description="Make sure to pick up gramaphone from bottom of gen 6 tunnel.", goal="Origins")

        # ------------------ ORIGINS: WIND STAFF ---------------------
        wind_disk = Task(title="Collect Yellow Disk (Wind Record)", description="Locations (Gen 5 area) : \n - On the wall next to Stamin-Up\n - On the crates next to Gen 5\n - Directly to the left after entering the Gen 5 tunnel on bench (Lightning tunnel)", goal="Origins")
        wind_p_spawn = Task(title="Collect Wind Staff part (Spawn robot)", description="Enter the spawn giant 'Thor' (Spawn/Gen 2/Gen 3 path) by standing in giant footprint and shooting glowing circle on bottom of foot as giant steps on you.\n*NOTE* Try to look at the bottom of the giants foot as it walks towards you, only one of the feet will be glowing", goal="Origins")
        wind_p_nml = Task(title="Collect Wind Staff part (NML robot)", description="Enter the middle giant 'Odin' (Center area/Gen 4/Gen 5/No mans land) by standing in giant footprint and shooting glowing circle on bottom of foot as giant steps on you.\n*NOTE* Try to look at the bottom of the giants foot as it walks towards you, only one of the feet will be glowing", goal="Origins")
        wind_p_church = Task(title="Collect Wind Staff part (Church robot)", description="Enter the church giant 'Freya' (Church area) by standing in giant footprint and shooting glowing circle on bottom of foot as giant steps on you.\n*NOTE* Try to look at the bottom of the giants foot as it walks towards you, only one of the feet will be glowing", goal="Origins")
        wind_portal = Task(title="Enter Wind Portal & Retrieve Gem", description="Place gramophone at Gen 4 tunnel. Retrieve the Yellow Gem from wind pedestal and exit. *NOTE* You may have left gramophone somewhere else (Go pick it up)", goal="Origins")
        build_wind = Task(title="Build Wind Staff", description="Build at the Yellow Altar in the lower excavation.", goal="Origins")
        wind_puzzle = Task(title="Solve Wind Puzzle (Crazy Place)", description="Rotate the rings on the ceiling to match the correct symbols. (IN PROGRESS)", goal="Origins")
        wind_smoke = Task(title="Redirect 3 Smoke Vents", description="Shoot the 3 smoking balls with the Wind Staff so the smoke faces the center mound. \nLocations : \n - In between wind tunnel and gen 4\n - Up the tank return path near lower church\n - In between gen 5 and mound", goal="Origins")
        wind_orb = Task(title="Align Gems & Shoot Yellow Orb", description="Rotate all the rings in lower excavation to YELLOW using the glowing levers in lower excavation, then shoot the yellow orb at the bottom with wind staff.", goal="Origins")
        wind_altar = Task(title="Place Staff in Wind Altar", description="Return to the Crazy Place and place the wind staff in the wind pedestal.", goal="Origins")
        wind_portal_exit = Task(title="(WIND) Exit crazy place *READ DESC*", description="At this point you can either:\nA. Leave the crazy place and upgrade all the staffs at the same time later.\nB. Upgrade the wind staff by getting kills in the crazy place while it is in the altar", goal="Origins")
        retrieve_gram_wind = Task(title="Pick up gramophone (WIND tunnel) (Gen 4)", description="Make sure to pick up gramophone from bottom of gen 4 tunnel.", goal="Origins")

        # ------------------ ORIGINS: LIGHTNING STAFF ------------------
        light_disk = Task(title="Collect Purple Disk (Lightning Record)", description="Locations (Gen 4 area) : \n - On wheelbarrow next to Gen 4\n - Bench next to Perk-a-Cola near Gen 4\n - Bottom of Gen 4 Wind Tunnel", goal="Origins")
        light_p_tank1 = Task(title="Collect Lightning Staff part (Tank exit right)", description="Ride the tank from church, jump onto wooden structure on the right.", goal="Origins")
        light_p_tank2 = Task(title="Collect Lightning Staff part (Tank return left)", description="Ride the tank from tank station, jump onto wooden structure next to mound on the left.", goal="Origins")
        light_p_tank3 = Task(title="Collect Lightning Staff part (Tank return right)", description="Ride the tank from tank station, jump to the right on path near church.", goal="Origins")
        light_dials = Task(title="Adjust all 7 lightning dials", description="Turn dials to these positions : \n - Gen 1 : LEFT\n - Tank Station ( Next to Gen 2) : DOWN\n - Gen 4 : UP\n - Mound (Near church entrance against mound) : UP\n - Gen 5 : DOWN\n - Lower Church : RIGHT\n - Upper Church : UP", goal="Origins")
        light_portal = Task(title="Enter Lightning Portal & Retrieve Gem", description="Place gramophone at Gen 5 tunnel. Retrieve the Purple Gem from lightning pedestal and exit. *NOTE* You may have left gramophone somewhere else (Go pick it up)", goal="Origins")
        build_light = Task(title="Build Lightning Staff", description="Build at the Purple Altar in the lower excavation.", goal="Origins")
        light_puzzle = Task(title="Solve Lightning Puzzle (Crazy Place)", description="Steps : \n - Look at triangles near portal (triangle facing DOWN)\n - From left to right triangles are numbered 1-7\n - Shoot triangles in this order with lightning staff :\n   - 1, 3, 6\n   - 3, 5, 7\n   - 2, 4, 6", goal="Origins")
        light_orb = Task(title="Align Gems & Shoot Purple Orb", description="Rotate all the rings in lower excavation to PURPLE using the glowing levers, then shoot the purple orb at the bottom with lightning staff.", goal="Origins")
        light_altar = Task(title="Place Staff in Lightning Altar", description="Return to the Crazy Place and place the lightning staff in the lightning pedestal.", goal="Origins")
        light_portal_exit = Task(title="(LIGHTNING) Exit crazy place *READ DESC*", description="At this point you can either:\nA. Leave the crazy place and upgrade all the staffs at the same time later.\nB. Upgrade the lightning staff by getting kills in the crazy place while it is in the altar", goal="Origins")
        retrieve_gram_light = Task(title="Pick up gramophone (LIGHTNING tunnel) (Gen 5)", description="Make sure to pick up gramophone from bottom of gen 5 tunnel.", goal="Origins")

        # ------------------ ORIGINS: FIRE STAFF ------------------
        fire_disk = Task(title="Collect Red Disk (Fire Record)", description="Locations (Gen 6 / Church area) : \n - In between the front left of tank, a crate, and the stone pillar\n - Upper church on a bench\n - Next to Gen 6 sign above a skeleton", goal="Origins")
        fire_p_plane = Task(title="Collect Fire Staff part (Flaming Plane)", description="Shoot down the glowing orange plane in the sky (appears the round after opening the Church entrance). Pick up the part near the Mound/Gen 4 path.", goal="Origins")
        fire_p_gen6 = Task(title="Collect Fire Staff part (Gen 6 Chest)", description="Capture Generator 6 and collect the part from the reward chest behind the church.", goal="Origins")
        fire_p_panzer = Task(title="Collect Fire Staff part (Round 8 Panzer)", description="Kill the Panzer Soldat (first spawns Round 8) and pick up the part he drops. *Note* Use one of the staffs to kill Panzer for a much easier fight", goal="Origins")
        fire_portal = Task(title="Enter Fire Portal & Retrieve Gem", description="Place gramophone at Gen 1 (Spawn) tunnel. Retrieve the Red Gem from fire pedestal and exit. *NOTE* You may have left gramophone somewhere else (Go pick it up)", goal="Origins")
        build_fire = Task(title="Build Fire Staff", description="Build at the Red Altar in the lower excavation.", goal="Origins")
        fire_sacrifice = Task(title="Kill Zombies on Grates (Crazy Place)", description="Stand on the metal grates near the 4 fire cauldrons in the Crazy Place. Kill zombies with the Fire Staff until all 4 cauldrons are lit.", goal="Origins")
        fire_puzzle = Task(title="Solve Fire Puzzle (Church)", description="Go to the church basement. Match the symbols on the wall to the 4 glowing torches upstairs. (IN PROGRESS)", goal="Origins")
        fire_orb = Task(title="Align Gems & Shoot Red Orb", description="Rotate all the rings in lower excavation to RED using the glowing levers in lower excavation, then shoot the red orb at the bottom with fire staff.", goal="Origins")
        fire_altar = Task(title="Place Staff in Fire Altar", description="Return to the Crazy Place and place the fire staff in the red pedestal.", goal="Origins")
        fire_portal_exit = Task(title="(FIRE) Exit crazy place *READ DESC*", description="At this point you can either:\nA. Leave the crazy place and upgrade all the staffs at the same time later.\nB. Upgrade the fire staff by getting kills in the crazy place while it is in the altar", goal="Origins")
        retrieve_gram_fire = Task(title="Pick up gramophone (FIRE tunnel) (Gen 1)", description="Make sure to pick up gramophone from bottom of gen 1 tunnel.", goal="Origins")

        # ------------------ ORIGINS: MELEE UPGRADE ------------------
        soul_boxes = Task(title="Fill 4 Soul Boxes", description="Soul box looks like a black box with pruple designs.\nFill boxes at :\n - Left church giant footprint\n - Gen 5 giant right footprint\n - Mound giant left footprint\n - Gen 4 giant right footprint", goal="Origins")
        one_inch_punch = Task(title="Collect One Inch Punch", description="Pick up your reward from the orange glowing chest at Gen 1 or Gen 6.", goal="Origins")

        # ------------------ ORIGINS: G-STRIKE (AIRSTRIKE) ------------------
        gs_collect = Task(title="Collect stone tablet from tank station", description="Located on bench in the back of the Tank Station near back exit. Tank station is located right next to gen 2.", goal="Origins")
        gs_place = Task(title="Place stone tablet in church holy water", description="On the upper floor of the church there is an elevated bowl near the benches, place stone tablet in bowl.", goal="Origins")
        gs_cleanse = Task(title="Cleanse stone tablet with melee kills", description="Get melee kills near the holy water bowl until the stone is clean. You will know it is clean once zombie souls no longer go into the bowl on melee kills. \n*NOTE* Using an upgraded staff melee makes this step much easier", goal="Origins")
        gs_carry = Task(title="Carry cleansed tablet to Tank Station", description="Take the cleansed tablet back to tank station where you found it (Bunker near gen 2).\n⚠️ WARNING: If you step in mud, you must return it to the church bowl to cleanse it (Do not need to refill souls).", goal="Origins")
        gs_bench = Task(title="Place tablet on Tank Station bench", description="Place cleansed tablet on bench in back of tank station that you got it from", goal="Origins")
        gs_kills = Task(title="Get melee kills near tablet at Tank Station ", description="Melee kill zombies near the bench until the G-Strikes appear on bench.", goal="Origins")
        gs_retrieve = Task(title="Retrieve Air Strike grenades", description="Interact with Air Strike grenades on bench to pick them up", goal="Origins")

        # ------------------ ORIGINS: LITTLE LOST GIRL (Phase 1) ------------------
        upgrade_all_staffs = Task(title="Wield the Ultimate Power (Upgrade all staffs)", description="All staffs must be in their pedestals in the Crazy Place. Get ~20 kills per staff in the Crazy Place until the staff icons on your HUD glow white. If you have already upgraded staffs in the previous steps use the upgraded staffs to upgrade the other staffs", goal="Origins")

        place_fire_mound = Task(title="Place Fire Staff in Mound", description="Place the upgraded Fire Staff into its slot at the very bottom of the Excavation Site (Pedestal in front of initial four staff pedestals).", goal="Origins")
        place_ice_church = Task(title="Place Ice Staff in Church Robot (Freya)", description="Enter the Church giant (Freya) and place the Ice Staff in the pedestal.", goal="Origins")
        place_wind_nml = Task(title="Place Wind Staff in NML Robot (Odin)", description="Enter the middle giant (Odin) and place the Wind Staff in the pedestal.", goal="Origins")
        place_light_spawn = Task(title="Place Lightning Staff in Spawn Robot (Thor)", description="Enter the spawn giant (Thor) and place the Lightning Staff in the pedestal.", goal="Origins")

        # ------------------ ORIGINS: RELEASING THE HORDE ------------------
        prep_airstrike = Task(title="Preparation for Horde Step", description="If you have not already, go get all your perks and PAP gun.\nAll staffs will respawn at bottom of excavation, grab one (Fire and lightning are best).\n(!) Now go to Gen 5 and look outside the map for the concrete patch near the left footprint of the Middle Giant. Make note of this.\nYou will also need Airstrike grenades for next stap (The stone tablet subquest).", goal="Origins")
        press_button = Task(title="Press Red Button inside Robot *READ DESC*", description="All 3 robots are now marching. You must press the button in robot head and throw the Airstrike grenades at concrete patch in quick succession.\nSOLO STRAT :\n 1. Enter the MIDDLE Giant (Odin) at the Gen 5 left or right footprint.\n 2. Wait for the countdown. Press the Red Button on '1'.\n 3. You will be ejected. Immediately sprint to the concrete seal and throw your Airstrike grenade.\nCo-op : \n 1. Have one player board any giant and one player on ground near concrete patch\n 2. Once ready, player in giant will press button and signal to ground player to throw airstrike grenade at concrete patch", goal="Origins")
        deploy_maxis_seal = Task(title="Deploy Maxis Drone at Seal", description="Once the seal is broken by the Airstrike, deploy the Maxis Drone near the crater. He will fly in and unleash the Panzer horde.", goal="Origins")
        kill_panzers = Task(title="Kill the Panzer Horde", description="As soon as Maxis enters the crater, multiple Panzers will drop into the map. Use upgraded staffs or a Ray Gun Mark II to clear them out quickly.", goal="Origins")

        # ------------------ ORIGINS: SKEWER THE WINGED BEAST ------------------
        get_zombie_blood = Task(title="Extinguish Flaming Carts (Zombie Blood)", description="Use the ICE STAFF to shoot the fire on 3 flaming wagons around the Mound. A Zombie Blood power-up will spawn at the pack-a-punch side of the mound.\n*NOTE* Cannot be done during rainy weather.\n *NOTE 2* The following steps will be done in quick succession, read ahead to ensure you complete them within the duration of the zombie blood", goal="Origins")
        shoot_plane_ee = Task(title="Shoot down flaming plane", description="While in Zombie Blood, look at the sky for a glowing red plane (similar to the fire part plane) and shoot it down.\n *NOTE* If you fail this step you will have to progress one round to obtain zombie blood from extinguished carts again", goal="Origins")
        kill_pilot_zombie = Task(title="Kill Invisible Pilot Zombie", description="While still in Zombie Blood, run counter-clockwise around the mound. An invisible zombie (now visible while in zombie blood) will be running clockwise toward you. Kill him, he should drop the maxis drone.\n *NOTE* If you fail this step you will have to progress one round to obtain zombie blood from extinguished carts again BUT this time you dont need to shoot down plane", goal="Origins")
        collect_upgraded_drone = Task(title="Pick up upgraded Maxis Drone", description="The pilot zombie will drop the upgraded Maxis Drone. Pick it up immediately.", goal="Origins")
        reclaim_drone = Task(title="Reclaim Maxis Drone from Bench", description="Go back to the workbench where you originally crafted the drone and pick it up one last time.", goal="Origins")

        # ------------------ ORIGINS: IRON FIST UPGRADE ------------------
        prep_fists = Task(title="Iron Fist Preparation", description="Ensure all 6 generators are currently active and you have the basic 'One Inch Punch' equipped from soul box subquest.", goal="Origins")
        iron_fist_kills = Task(title="Melee Zombies at bottom of Mound", description="Go to the very bottom of the Excavation site (near the staff pedestals). Melee zombies that have a white/misty glow around their arms. You must do this until a glowing white tablet appears. *NOTE* Upgraded staff melee works well for this", goal="Origins")
        collect_iron_fist = Task(title="Pick up Upgraded Iron Fist", description="Pick up the glowing white tablet to upgrade your melee to the elemental Iron Fist. This is required for the final step!", goal="Origins")

        # ------------------ ORIGINS: THE FINAL ENCOUNTER ------------------
        final_staff_deposit = Task(title="Deposit all Staffs in Crazy Place", description="Go to the Crazy Place and place all 4 upgraded staffs into their respective pedestals. \n*WARNING*: Once you start the next step, you cannot leave until it is finished.\n Now is a good time to PAP all your weapons and get your gobblegum of choice", goal="Origins")
        final_soul_harvest = Task(title="Sacrifice Souls (Final Harvest)", description="Kill zombies inside the Crazy Place using your weapons (Nukes don't count). You will need approximately 100 kills. The step is complete when the screen flashes white and the ceiling opens up.", goal="Origins")
        launch_maxis_final = Task(title="Send Maxis into the Light", description="Deploy the Maxis Drone in the center of the Crazy Place. He will fly up into the light. Step into the center portal to trigger the final cutscene and complete the Easter Egg!", goal="Origins")

        # --- BATCH ADD ALL TASKS ---
        all_tasks = [
            collect_shovel, s_handle, s_visor, s_frame, build_shield,
            gen1, gen2, gen3, gen4, gen5, gen6,
            d_rotor, d_brain, d_frame, build_drone,
            collect_white_record, collect_gramophone, place_gramophone, retrieve_gramophone,
            ice_disk, ice_p_spawn, ice_p_middle, ice_p_church, ice_portal, build_ice, 
            ice_puzzle, ice_graves, ice_orb, ice_altar, ice_portal_exit, retrieve_gram_ice,
            wind_disk, wind_p_spawn, wind_p_nml, wind_p_church, wind_portal, build_wind, 
            wind_puzzle, wind_smoke, wind_orb, wind_altar, wind_portal_exit, retrieve_gram_wind,
            light_disk, light_p_tank1, light_p_tank2, light_p_tank3, light_dials, light_portal, 
            build_light, light_puzzle, light_orb, light_altar, light_portal_exit, retrieve_gram_light,
            fire_disk, fire_p_plane, fire_p_gen6, fire_p_panzer, fire_portal, build_fire, 
            fire_sacrifice, fire_puzzle, fire_orb, fire_altar, fire_portal_exit, retrieve_gram_fire,
            soul_boxes, one_inch_punch,
            gs_collect, gs_place, gs_cleanse, gs_carry, gs_bench, gs_kills, gs_retrieve,
            upgrade_all_staffs, place_fire_mound, place_ice_church, place_wind_nml, place_light_spawn,
            prep_airstrike, press_button, deploy_maxis_seal, kill_panzers,
            get_zombie_blood, shoot_plane_ee, kill_pilot_zombie, collect_upgraded_drone, reclaim_drone,
            prep_fists, iron_fist_kills, collect_iron_fist,
            final_staff_deposit, final_soul_harvest, launch_maxis_final
        ]
        db.add_all(all_tasks)
        db.flush() 

        #DEPENDENCIES
        build_shield.depends_on.extend([s_handle, s_visor, s_frame])

        build_drone.depends_on.append(d_rotor)
        build_drone.depends_on.append(d_brain)
        build_drone.depends_on.append(d_frame)

        place_gramophone.depends_on.append(collect_gramophone)
        place_gramophone.depends_on.append(collect_white_record)
        retrieve_gramophone.depends_on.append(place_gramophone)

        ice_p_spawn.depends_on.append(collect_shovel)
        ice_p_middle.depends_on.append(collect_shovel)
        ice_p_church.depends_on.append(collect_shovel)

        ice_portal.depends_on.extend([ice_disk, collect_gramophone]) #To open ice portal you need ice disk and gramaphone
        build_ice.depends_on.extend([ice_portal, ice_p_spawn, ice_p_middle, ice_p_church, place_gramophone]) #To build ice staff you need to have gotten, gem and three parts
        ice_puzzle.depends_on.append(build_ice) #To start ice puzzle you need ice staff
        ice_graves.depends_on.append(ice_puzzle) #To begin graves puzzle you need to have done ice puzzle in crazy place
        ice_orb.depends_on.append(ice_graves) #To shoot ice orb you need to have done graves puzzle
        ice_altar.depends_on.append(ice_orb) #To place ice staff in altar you need to have shot ice orb
        ice_portal_exit.depends_on.append(ice_altar) #Not required but next logical step is to exit from ice portal and pickup gramaphone
        retrieve_gram_ice.depends_on.append(ice_portal_exit) #Once out of crazy place get gramaphone

        wind_portal.depends_on.extend([wind_disk, collect_gramophone]) 
        build_wind.depends_on.extend([wind_portal, wind_p_spawn, wind_p_nml, wind_p_church, place_gramophone])
        wind_puzzle.depends_on.append(build_wind)
        wind_smoke.depends_on.append(wind_puzzle)
        wind_orb.depends_on.append(wind_smoke)
        wind_altar.depends_on.append(wind_orb)
        wind_portal_exit.depends_on.append(wind_altar)
        retrieve_gram_wind.depends_on.append(wind_portal_exit)

        light_portal.depends_on.extend([light_disk, collect_gramophone]) 
        build_light.depends_on.extend([light_portal, light_p_tank1, light_p_tank2, light_p_tank3, place_gramophone])
        light_puzzle.depends_on.append(build_light)
        light_orb.depends_on.extend([light_puzzle, light_dials])
        light_altar.depends_on.append(light_orb)
        light_portal_exit.depends_on.append(light_altar)
        retrieve_gram_light.depends_on.append(light_portal_exit)

        fire_p_gen6.depends_on.append(gen6)
        fire_portal.depends_on.extend([fire_disk, collect_gramophone]) 
        build_fire.depends_on.extend([fire_portal, fire_p_plane, fire_p_gen6, fire_p_panzer, place_gramophone])
        fire_sacrifice.depends_on.append(build_fire)
        fire_puzzle.depends_on.append(fire_sacrifice)
        fire_orb.depends_on.append(fire_puzzle)
        fire_altar.depends_on.append(fire_orb)
        fire_portal_exit.depends_on.append(fire_altar)
        retrieve_gram_fire.depends_on.append(fire_portal_exit)

        one_inch_punch.depends_on.append(soul_boxes)

        gs_place.depends_on.append(gs_collect)
        gs_cleanse.depends_on.append(gs_place)
        gs_carry.depends_on.append(gs_cleanse)
        gs_bench.depends_on.append(gs_carry)
        gs_kills.depends_on.append(gs_bench)
        gs_retrieve.depends_on.append(gs_kills)

        upgrade_all_staffs.depends_on.extend([ice_altar, wind_altar, light_altar, fire_altar])

        final_placements = [place_fire_mound, place_ice_church, place_wind_nml, place_light_spawn]
        place_fire_mound.depends_on.append(upgrade_all_staffs)
        place_ice_church.depends_on.append(upgrade_all_staffs)
        place_wind_nml.depends_on.append(upgrade_all_staffs)
        place_light_spawn.depends_on.append(upgrade_all_staffs)

        prep_airstrike.depends_on.extend([place_fire_mound, place_ice_church, place_wind_nml, place_light_spawn])
        press_button.depends_on.extend([prep_airstrike, gs_retrieve])
        deploy_maxis_seal.depends_on.extend([press_button, build_drone])
        kill_panzers.depends_on.append(deploy_maxis_seal)

        get_zombie_blood.depends_on.append(kill_panzers)
        shoot_plane_ee.depends_on.append(get_zombie_blood)
        kill_pilot_zombie.depends_on.append(shoot_plane_ee)
        collect_upgraded_drone.depends_on.append(kill_pilot_zombie)
        reclaim_drone.depends_on.append(collect_upgraded_drone)

        prep_fists.depends_on.append(reclaim_drone) 
        iron_fist_kills.depends_on.extend([prep_fists, gen1, gen2, gen3, gen4, gen5, gen6, one_inch_punch])
        collect_iron_fist.depends_on.append(iron_fist_kills)

        final_staff_deposit.depends_on.append(collect_iron_fist)
        final_soul_harvest.depends_on.append(final_staff_deposit)
        launch_maxis_final.depends_on.append(final_soul_harvest)

        # ------------------ ORIGINS COMMIT ------------------
        db.commit()
        print(f"Successfully seeded {len(all_tasks)} tasks for Origins!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()