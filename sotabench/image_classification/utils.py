import time

from sotabench.utils import AverageMeter, accuracy


def get_classification_metrics(model, test_loader, criterion, is_cuda=True):
    batch_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()
    top5 = AverageMeter()

    end = time.time()

    for i, (input, target) in enumerate(test_loader):

        if is_cuda:
            target = target.cuda(non_blocking=True)
            input = input.cuda()

        # compute output
        output = model(input)
        loss = criterion(output, target)
        prec1, prec5 = accuracy(output, target, topk=(1, 5))
        losses.update(loss.data.item(), input.size(0))
        top1.update(prec1.item(), input.size(0))
        top5.update(prec5.item(), input.size(0))
        batch_time.update(time.time() - end)
        end = time.time()

    return {
        'top_1_accuracy': top1.avg,
        'top_5_accuracy': top5.avg
    }