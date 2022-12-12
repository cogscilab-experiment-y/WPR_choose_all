from code.load_data import read_text_from_file
from code.check_exit import check_exit
from psychopy import visual, gui, event, clock


def part_info(test=False):
    if test:
        info = {'Kod badanego': '', 'Wiek': '20', 'Płeć': 'M'}
    else:
        info = {'Kod badanego': '', 'Wiek': '', 'Płeć': ['M', "K"]}
        dict_dlg = gui.DlgFromDict(dictionary=info, title='WPR')
        if not dict_dlg.OK:
            exit(1)
    info = {'Part_id': info['Kod badanego'],
            'Part_age': info["Wiek"],
            'Part_sex': info["Płeć"]}
    return info, f"{info['Part_id']}_{info['Part_sex']}_{info['Part_age']}"


def show_info(win, file_name, text_size, text_color, screen_res, insert=''):
    msg = read_text_from_file(file_name, insert=insert)
    msg = visual.TextStim(win, color=text_color, text=msg, height=text_size, wrapWidth=screen_res['width'])
    msg.draw()
    win.flip()
    key = event.waitKeys(keyList=['f7', 'return', 'space'])
    if key == ['f7']:
        raise Exception('Experiment finished by user on info screen! F7 pressed.')
    win.flip()


def show_clock(clock_image, trial_clock, config):
    if config["show_clock"] and trial_clock.getTime() > config["clock_show_time"]:
        clock_image.draw()


def show_timer(timer, trial_clock, config):
    if config["show_timer"]:
        timer.setText(config["answer_time"] - int(trial_clock.getTime()))
        timer.draw()


def draw_stim_list(stim_list: list, flag: bool):
    for elem in stim_list:
        elem.setAutoDraw(flag)


def show_stim(stim, stim_time: int, trial_clock: clock.Clock, win: visual.Window):
    if stim_time == 0:
        return
    if stim is not None:
        stim.draw()
    win.callOnFlip(trial_clock.reset)
    win.callOnFlip(event.clearEvents)
    win.flip()
    while trial_clock.getTime() < stim_time:
        if stim is not None:
            stim.draw()
        check_exit()
        win.flip()

    win.flip()
