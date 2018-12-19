import itertools
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix

def _get_hist_at(histories, t_epoch):
    acc = []
    loss = []
    val_acc = []
    val_loss = []

    for i in histories:
        acc.append(i.history['acc'][t_epoch])
        loss.append(i.history['loss'][t_epoch])
        val_acc.append(i.history['val_acc'][t_epoch])
        val_loss.append(i.history['val_loss'][t_epoch])
    
    return acc, loss, val_acc, val_loss

def visualize_history(history):
    # summarize history for accuracy
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

def plot_complexty_graph_at_epoch(histories, t_epoch, complexities):
    _, _, val_acc, val_loss = _get_hist_at(histories, t_epoch)
        
    # summarize history validation acc
    plt.plot(val_acc)
    plt.title('Complexity-Validation Accuracy (at {}. epoch)'.format(t_epoch))
    plt.ylabel('Validation accuracy')
    plt.xlabel('Complexity (neuron count)')
    plt.xticks(range(len(complexities)), [str(i) for i in complexities])
    plt.legend(['Validation Accuracy'], loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()
    
    # summarize history for validation loss
    plt.plot(val_loss)
    plt.title('Complexity-Validation Loss (at {}. epoch)'.format(t_epoch))
    plt.ylabel('Validation loss')
    plt.xlabel('Complexity (neuron count)')
    plt.xticks(range(len(complexities)), [str(i) for i in complexities])
    plt.legend(['Validation Loss'], loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

def plot_unified_complexity_graph(histories, epochs, complexities):
    legends = []
    for epoch in epochs:
        _, _, val_acc, _ = _get_hist_at(histories, epoch)
      
        plt.plot(val_acc)
        legends.append('{}. Epoch'.format(epoch))


    plt.title('Complexity-Validation Accuracy')
    plt.ylabel('Validation accuracy')
    plt.xlabel('Complexity (neuron count)')
    plt.xticks(range(len(complexities)), [str(i) for i in complexities])
    plt.legend(legends, loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

    legends = []
    for epoch in epochs:
        _, _, _, val_loss = _get_hist_at(histories, epoch)

        plt.plot(val_loss)
        legends.append('{}. Epoch'.format(epoch))
    
    # summarize history for validation loss
    plt.title('Complexity-Validation Loss')
    plt.ylabel('Validation loss')
    plt.xlabel('Complexity (neuron count)')
    plt.xticks(range(len(complexities)), [str(i) for i in complexities])
    plt.legend(legends, loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

def plot_confusion_matrix(test_labels, predicted_labes):
    def get_action_list():
        tmp = {}
        labels = te_labels.argmax(axis=1)
        for l in labels:
            tmp[DISTINCT_ACTIONS[l]] = l

        def find_min(dic):
            _min = len(DISTINCT_ACTIONS) + 1
            key = None
            for item, index in dic.items():
                if index < _min:
                    _min = index
                    key = item
            del tmp[key]
            return _min

        actions = []
        while(tmp.keys()):
            actions.append(DISTINCT_ACTIONS[find_min(tmp)])

        return actions
    
    def plot(cm, classes, normalize=True, title='Confusion matrix', cmap=plt.cm.Blues):
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=90)
        plt.yticks(tick_marks, classes)

        fmt = '.1f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, format(cm[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

        plt.ylabel('True label')
        plt.xlabel('Predicted label')
    
    cnf_matrix = confusion_matrix(te_labels.argmax(axis=1), y_pred.argmax(axis=1))
    
    plt.figure(figsize=(14, 14))
    plot(cnf_matrix, classes=get_action_list())
    plt.show()