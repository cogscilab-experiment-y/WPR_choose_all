import atexit
import csv
import random
from os.path import join
from psychopy import visual, core, event


from code.load_data import load_config
from code.screen_misc import get_screen_res
from code.show_info import part_info, show_info, show_stim, show_clock, show_timer, draw_stim_list
from code.block import prepare_block
from code.trial import Trial
from code.check_exit import check_exit


RESULTS = []
PART_ID = ""


@atexit.register
def save_beh_results():
    num = random.randint(100, 999)
    with open(join('results', '{}_beh_{}.csv'.format(PART_ID, num)), 'w', newline='') as beh_file:
        dict_writer = csv.DictWriter(beh_file, RESULTS[0].keys(), delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(RESULTS)


def run_trial(win, trial, config, fixation, trial_clock, extra_text, clock_image, timer, show_feedback, feedback_text, block_type, mouse, trail_idx):
    answer = []
    reaction_time = None
    acc = -1
    mouse.setVisible(False)

    # fixation
    if config["fixation_time"] > 0:
        show_stim(fixation, config["fixation_time"], trial_clock, win)

    win.callOnFlip(trial_clock.reset)
    win.callOnFlip(event.clearEvents)

    show_stim(trial.matrix_1, config["matrix_1_time"], trial_clock, win)
    show_stim(trial.mask, config["mask_time"], trial_clock, win)

    draw_stim_list(extra_text, True)
    trial_clock.reset()
    win.callOnFlip(trial_clock.reset)
    trial.matrix_2.setAutoDraw(True)
    mouse.setPos(config["stimulus_central_pos"])
    mouse.setVisible(True)
    while trial_clock.getTime() < config["matrix_2_time"] and len(answer) < trial.matrix_1.n:
        show_clock(clock_image, trial_clock, config)
        show_timer(timer, trial_clock, config)
        for stimulus in trial.matrix_2.stimulus_to_draw:
            if mouse.isPressedIn(stimulus["stim_to_draw"]) and stimulus["stimulus"] not in answer:
                stimulus["stim_border"].setAutoDraw(True)
                reaction_time = trial_clock.getTime()
                answer.append(stimulus["stimulus"])
            elif stimulus["stim_to_draw"].contains(mouse):
                stimulus["stim_border"].draw()
        check_exit()
        win.flip()
    trial.matrix_2.setAutoDraw(False)
    mouse.setVisible(False)
    all_stimulus = sum([1 for stim in trial.matrix_1.stimulus_to_draw if stim["stimulus"] in answer])
    if answer:
        acc = all_stimulus/trial.matrix_1.n

    trial_results = {"idx": trail_idx,
                     "n": trial.matrix_1.n,
                     "size": [trial.matrix_1.size_y, trial.matrix_1.size_x],
                     "block_type": block_type,
                     "rt": reaction_time,
                     "acc": acc,
                     "correct_answers": all_stimulus,
                     "number_of_answers": len(answer),
                     "answer": answer,
                     "stimulus": [stim["stimulus"] for stim in trial.matrix_1.stimulus_to_draw]}
    RESULTS.append(trial_results)

    draw_stim_list(extra_text, False)
    if show_feedback:
        if acc == -1:
            text = feedback_text["no_answer"]
        else:
            text = feedback_text["answer"].replace("{}", str(all_stimulus), 1)
            text = text.replace("{}", str(trial.matrix_1.n), 1)
        feedback = visual.TextBox2(win, color=config["fdbk_color"], text=text, letterHeight=config["fdbk_size"], alignment="center")
        show_stim(feedback, config["fdbk_show_time"], trial_clock, win)

    wait_time = config["wait_time"] + random.random() * config["wait_jitter"]
    show_stim(None, wait_time, trial_clock, win)


def run_block(win, config, trials, stimulus_list, block_type, show_feedback,
              fixation, clock, extra_text, clock_image, timer, feedback_text, mouse):
    for trail_idx, trial in enumerate(trials):
        stimulus_to_use = random.sample(stimulus_list, trial["size"][0]*trial["size"][1])
        chosen_stimulus = random.sample(stimulus_to_use, trial["n"])
        t = Trial(win=win, config=config, n=trial["n"], size=trial["size"], group_elements=trial["group_elements"])
        t.matrix_1.prepare_to_draw(stimulus_list=chosen_stimulus, stimulus_type=config["stimulus_type"], win=win,
                                   border_width=config["stimulus_border_width"], border_color=config["stimulus_border_color"])
        t.matrix_2.prepare_to_draw(stimulus_list=stimulus_to_use, stimulus_type=config["stimulus_type"], win=win,
                                   border_width=config["stimulus_border_width"], border_color=config["stimulus_border_color"])
        run_trial(win=win, trial=t, config=config, fixation=fixation, trial_clock=clock, extra_text=extra_text, clock_image=clock_image,
                  timer=timer, feedback_text=feedback_text, show_feedback=show_feedback, block_type=block_type, mouse=mouse, trail_idx=trail_idx)


def main():
    global PART_ID
    config = load_config()
    info, PART_ID = part_info(test=config["procedure_test"])

    screen_res = dict(get_screen_res())
    win = visual.Window(list(screen_res.values()), fullscr=True, units='pix', screen=0, color=config["screen_color"])
    mouse = event.Mouse()

    clock = core.Clock()

    fixation = visual.TextBox2(win, color=config["fixation_color"], text=config["fixation_text"],
                               letterHeight=config["fixation_size"], pos=config["fixation_pos"],
                               alignment="center")

    clock_image = visual.ImageStim(win, image=join('images', 'clock.png'), interpolate=True,
                                   size=config['clock_size'], pos=config['clock_pos'])

    timer = visual.TextBox2(win, color=config["timer_color"], text=config["matrix_2_time"],
                            letterHeight=config["timer_size"], pos=config["timer_pos"], alignment="center")

    extra_text = [visual.TextBox2(win, color=text["color"], text=text["text"], letterHeight=text["size"],
                                  pos=text["pos"], alignment="center")
                  for text in config["extra_text_to_show"]]

    if info["Part_sex"] == "M":
        feedback_text = {"answer": config["fdbk_correctness_male"], "no_answer": config["fdbk_no_answer"]}
    else:
        feedback_text = {"answer": config["fdbk_correctness_female"], "no_answer": config["fdbk_no_answer"]}

    if config["stimulus_type"] == "image":
        stimulus_list = [join("images", "all_png", elem) for elem in config["stimulus_list"]]
    elif config["stimulus_type"] == "text":
        stimulus_list = config["stimulus_list"]
    else:
        raise Exception("Unknown stimulus_type. Chose from [image, text]")

    experiment_trials = prepare_block(config["experiment_trials"], randomize=config["experiment_randomize"])

    # run training
    if config["do_training"]:
        training_trials = prepare_block(config["training_trials"], randomize=config["training_randomize"])

        show_info(win, join('.', 'messages', 'instruction_training.txt'), text_color=config["text_color"],
                  text_size=config["text_size"], screen_res=screen_res)

        run_block(win=win, config=config, trials=training_trials, stimulus_list=stimulus_list, block_type="training", fixation=fixation,
                  clock=clock, extra_text=extra_text, clock_image=clock_image, timer=timer, feedback_text=feedback_text, mouse=mouse,
                  show_feedback=config["fdbk_training"])

    # run experiment
    show_info(win, join('.', 'messages', 'instruction_experiment.txt'), text_color=config["text_color"],
              text_size=config["text_size"], screen_res=screen_res)

    run_block(win=win, config=config, trials=experiment_trials, stimulus_list=stimulus_list, block_type="experiment", fixation=fixation,
              clock=clock, extra_text=extra_text, clock_image=clock_image, timer=timer, feedback_text=feedback_text, mouse=mouse,
              show_feedback=config["fdbk_experiment"])

    # end
    show_info(win, join('.', 'messages', 'end.txt'), text_color=config["text_color"],
              text_size=config["text_size"], screen_res=screen_res)


if __name__ == "__main__":
    main()
