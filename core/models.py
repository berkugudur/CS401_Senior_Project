import os, csv, datetime, copy
import pandas as pd
import matplotlib.pyplot as plt

ACTION_MAP2 = {
    'BASE': ['AIR', 'CROUCH', 'STAND'],
    'MOVE': ['BACK_JUMP', 'BACK_STEP', 'DASH', 'FOR_JUMP', 'FORWARD_WALK', 'JUMP'],
    'GUARD': ['AIR_GUARD', 'CROUCH_GUARD', 'STAND_GUARD'],
    'RECOV': ['AIR_GUARD_RECOV', 'AIR_RECOV', 'CHANGE_DOWN', 'CROUCH_GUARD_RECOV', 'CROUCH_RECOV', 'DOWN', 'LANDING',
              'RISE', 'STAND_GUARD_RECOV', 'STAND_RECOV', 'THROW_HIT', 'THROW_SUFFER'],
    'SKILL': ['AIR_A', 'AIR_B', 'AIR_DA', 'AIR_DB', 'AIR_FA', 'AIR_D_DB_BA', 'AIR_D_DB_BB', 'AIR_D_DF_FA', 'AIR_D_DF_FB',
              'AIR_FA', 'AIR_FB', 'AIR_F_D_DFA', 'AIR_F_D_DFB', 'AIR_UA', 'AIR_UB', 'CROUCH_A', 'CROUCH_B', 'CROUCH_FA',
              'CROUCH_FB', 'STAND_A', 'STAND_B', 'STAND_FA', 'STAND_FB', 'STAND_D_DB_BA', 'STAND_D_DB_BB', 'STAND_D_DF_FA',
              'STAND_D_DF_FB', 'STAND_D_DF_FC', 'STAND_F_D_DFA', 'STAND_F_D_DFB', 'THROW_A', 'THROW_B'],
    'ALL': []
}

class Table(pd.DataFrame):
    def __init__(self, data, columns):
        pd.DataFrame.__init__(self, data=data)
        # Remove last column
        del self[len(self.columns)-1]
        self.columns = columns

class GameData:
    def __init__(self, columns):
        self.rounds = []
        self.columns = columns
        
    def add_round(self, frames):
        self.rounds.append(frames)
        
    def get_column(self, column_name):
        col_index = self.columns.index(column_name)
        # Control null check
        frames = []
        for round in self.rounds:
            frames.extend([item[col_index] for item in round])
        return frames
        
    def filter(self, f):
        len_before = len(self)
        for i, round_data in enumerate(self.rounds):
            self.rounds[i] = f(self.columns, round_data)
        return len_before - len(self)
    
    # if count 3, x-3, x-2 .. x .. x+2, x+3 will be added
    def add_distortion(self, count, action_type):
        len_before = len(self)
        for i, round_data in enumerate(self.rounds):
            self.rounds[i] = self.distortion(self.columns, round_data, count, action_type)
        return len_before - len(self)
    
    def distortion(self, columns, round_data,count,action_type):
        prepared_frames = []
        for current_frame in round_data:
            if current_frame[columns.index("P2-action")] in ACTION_MAP2[action_type] or action_type == "ALL":
                for i in range(-count, count+1,1):
                    tmp = current_frame.copy()
                    tmp[columns.index("P1-x")] += i
                    tmp[columns.index("P2-x")] += i
                    prepared_frames.append(tmp)
            else:   
                prepared_frames.append(current_frame)
        return prepared_frames

    def table(self):
         return [Table(data=item, columns=self.columns) for item in self.rounds]

    def append(self, to_append):
        self.rounds.extend(to_append.rounds)

    def export_csv(self, file_name="game_data_export", columns=None):
        def extract_cols(frame, columns):
            extracted = []
            for column in columns:
                extracted.append(frame[column])
            return extracted;

        def create_file_name():
            # Control existance of out folder
            out_folder = "out/"
            if not os.path.exists(out_folder):
                os.makedirs(out_folder)

            time = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
            return out_folder + file_name + "_" + time + ".csv"

        file_name = create_file_name()
        writer = csv.writer(open(file_name, "w"), delimiter=',')

        # Write columns names
        writer.writerow(["Index"] + (columns if columns else self.columns))

        for i, frame in enumerate(self):
            row = extract_cols(frame, columns) if columns else frame
            writer.writerow([i] + row)

    def clone(self):
        return copy.deepcopy(self)

    def statistics(self):
        def get_statistics_of_round(rounds):
            p1_actions = []
            p2_actions = []
            for round in rounds:
                p1_actions = p1_actions + [frame[self.columns.index('P1-action')] for frame in round]
                p2_actions = p2_actions + [frame[self.columns.index('P2-action')] for frame in round]
            return Statistic(p1_actions), Statistic(p2_actions)
		
        return get_statistics_of_round(self.rounds)

    def __iter__(self):
        self.iterator_count = 0
        return self

    def __next__(self):
        def round_index():
            cumulative_sum = 0
            for i, r in enumerate(self.rounds):
                cumulative_sum += len(r)
                if self.iterator_count < cumulative_sum:
                    return i

        def frame_index(round_index):
            prev_round_len = 0 if round_index == 0 else sum([len(r) for i, r in enumerate(self.rounds) if i < round_index])
            return self.iterator_count - prev_round_len

        if self.iterator_count < len(self):
            r_index = round_index()
            f_index = frame_index(r_index)
            self.iterator_count += 1
            return dict(zip(self.columns, self.rounds[r_index][f_index]))
        else:
            raise StopIteration

    def __len__(self):
        return sum([len(round) for round in self.rounds])

    def __str__(self):
        return "There are {} rounds and {} frames.".format(len(self.rounds), len(self))


class Statistic:
    def __init__(self, actions):
        self.actions = actions
        self.distributions = dict()

        for action in actions:
            self.distributions[action] = self.distributions.get(action, 0) + 1

    def get_count_of_action(self, action):
        count = self.distributions.get(action, None)
        if count:
            return count
        raise ValueError('This action not exists {}'.format(action))

    def get_distribution_of_action(self, action):
        count = self.get_count_of_action(action)
        return float(count) / float(len(self.actions)) * 100

    def graph(self):
        plt.bar(range(len(self.distributions)), list(self.distributions.values()), align='center')
        plt.xticks(range(len(self.distributions)), list(self.distributions.keys()), rotation=70)
        plt.tight_layout()
        return plt

    def __str__(self):
        msg = ''
        for action, count in self.distributions.items():
            msg += '{},{},{}%\n'.format(
                action, 
                count, 
                self.get_distribution_of_action(action)
                )
        return msg
