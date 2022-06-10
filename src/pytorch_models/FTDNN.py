import torch
import torch.nn as nn
import torch.nn.functional as F
from IPython import embed

class FTDNNLayer(nn.Module):

    def __init__(self, semi_orth_in_dim, semi_orth_out_dim, affine_in_dim, out_dim, time_offset, dropout_p=0, device='cpu'):
        '''
        3 stage factorised TDNN http://danielpovey.com/files/2018_interspeech_tdnnf.pdf
        '''
        super(FTDNNLayer, self).__init__()
        self.semi_orth_in_dim = semi_orth_in_dim
        self.semi_orth_out_dim = semi_orth_out_dim
        self.affine_in_dim = affine_in_dim
        self.out_dim = out_dim
        self.time_offset = time_offset
        self.dropout_p = dropout_p
        self.device = device


        self.sorth = nn.Linear(self.semi_orth_in_dim, self.semi_orth_out_dim, bias=False)
        self.affine = nn.Linear(self.affine_in_dim, self.out_dim, bias=True) 
        self.nl = nn.ReLU()
        self.bn = nn.BatchNorm1d(out_dim, affine=False, eps=0.001)
        self.dropout = nn.Dropout(p=self.dropout_p)

    def forward(self, x):
        time_offset = self.time_offset
        if time_offset != 0:
            padding = x[:,0,:][:,None,:]
            xd = torch.cat([padding]*time_offset+[x], axis=1)
            xd = xd[:,:-time_offset,:]
            x = torch.cat([xd, x], axis=2)
        x = self.sorth(x)
        if time_offset != 0:
            padding = x[:,-1,:][:,None,:]
            padding = torch.zeros(padding.shape)
            if self.device == 'cuda':
                padding = padding.cuda()
            xd = torch.cat([x]+[padding]*time_offset, axis=1)
            xd = xd[:,time_offset:,:]
            x = torch.cat([x, xd], axis=2)
        x = self.affine(x)
        x = self.nl(x)
        x = x.transpose(1,2)
        x = self.bn(x).transpose(1,2)
        x = self.dropout(x)
        return x

class InputLayer(nn.Module):

    def __init__(
        self,
        input_dim=220,
        output_dim=1536,
        dropout_p=0):

        super(InputLayer, self).__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.dropout_p = dropout_p

        self.lda = nn.Linear(self.input_dim, self.input_dim)
        self.kernel = nn.Linear(self.input_dim,
                                self.output_dim)

        self.nonlinearity = nn.ReLU()
        self.bn = nn.BatchNorm1d(output_dim, affine=False, eps=0.001)
        self.drop = nn.Dropout(p=self.dropout_p)

    def forward(self, x):

        mfccs = x[:,:,:40]
        ivectors = x[:,:,-100:]
        padding_first = mfccs[:,0,:][:,None,:]
        padding_last = mfccs[:,-1,:][:,None,:]
        context_first = torch.cat([padding_first, mfccs[:,:-1,:]], axis=1)
        context_last = torch.cat([mfccs[:,1:,:], padding_last], axis=1)
        x = torch.cat([context_first, mfccs, context_last, ivectors], axis=2)
        x = self.lda(x)
        x = self.kernel(x)
        x = self.nonlinearity(x)

        x = x.transpose(1, 2)
        x = self.bn(x).transpose(1,2)
        x = self.drop(x)
        return x

def sum_outputs_and_feed_to_layer(x, x_2, layer):
        x_3 = x*0.75 + x_2
        x = x_3
        x_2 = layer(x_3)
        return x, x_2

class FTDNN(nn.Module):

    def __init__(self, in_dim=220, batchnorm=None, dropout_p=0, device_name='cpu'):

        super(FTDNN, self).__init__()

        self.layer01 = InputLayer(input_dim=in_dim, output_dim=1536)
        self.layer02 = FTDNNLayer(3072, 160, 320, 1536, 1, dropout_p=dropout_p, device=device_name)
        self.layer03 = FTDNNLayer(3072, 160, 320, 1536, 1, dropout_p=dropout_p, device=device_name)
        self.layer04 = FTDNNLayer(3072, 160, 320, 1536, 1, dropout_p=dropout_p, device=device_name)
        self.layer05 = FTDNNLayer(1536, 160, 160, 1536, 0, dropout_p=dropout_p, device=device_name)
        self.layer06 = FTDNNLayer(3072, 160, 320, 1536, 3, dropout_p=dropout_p, device=device_name)
        self.layer07 = FTDNNLayer(3072, 160, 320, 1536, 3, dropout_p=dropout_p, device=device_name)
        self.layer08 = FTDNNLayer(3072, 160, 320, 1536, 3, dropout_p=dropout_p, device=device_name)
        self.layer09 = FTDNNLayer(3072, 160, 320, 1536, 3, dropout_p=dropout_p, device=device_name)
        self.layer10 = FTDNNLayer(3072, 160, 320, 1536, 3, dropout_p=dropout_p, device=device_name)
        self.layer11 = FTDNNLayer(3072, 160, 320, 1536, 3, dropout_p=dropout_p, device=device_name)
        self.layer12 = FTDNNLayer(3072, 160, 320, 1536, 3, dropout_p=dropout_p, device=device_name)
        self.layer13 = FTDNNLayer(3072, 160, 320, 1536, 3, dropout_p=dropout_p, device=device_name)
        self.layer14 = FTDNNLayer(3072, 160, 320, 1536, 3, dropout_p=dropout_p, device=device_name)
        self.layer15 = FTDNNLayer(3072, 160, 320, 1536, 3, dropout_p=dropout_p, device=device_name)
        self.layer16 = FTDNNLayer(3072, 160, 320, 1536, 3, dropout_p=dropout_p, device=device_name)
        self.layer17 = FTDNNLayer(3072, 160, 320, 1536, 3, dropout_p=dropout_p, device=device_name)
        self.layer18 = nn.Linear(1536, 256, bias=False) #This is the prefinal-l layer
        
    def forward(self, x):

        '''
        Input must be (batch_size, seq_len, in_dim)
        '''
        x = self.layer01(x)
        x_2 = self.layer02(x)
        x, x_2 = sum_outputs_and_feed_to_layer(x, x_2, self.layer03)
        x, x_2 = sum_outputs_and_feed_to_layer(x, x_2, self.layer04)
        x, x_2 = sum_outputs_and_feed_to_layer(x, x_2, self.layer05)
        x, x_2 = sum_outputs_and_feed_to_layer(x, x_2, self.layer06)
        x, x_2 = sum_outputs_and_feed_to_layer(x, x_2, self.layer07)
        x, x_2 = sum_outputs_and_feed_to_layer(x, x_2, self.layer08)
        x, x_2 = sum_outputs_and_feed_to_layer(x, x_2, self.layer09)
        x, x_2 = sum_outputs_and_feed_to_layer(x, x_2, self.layer10)
        x, x_2 = sum_outputs_and_feed_to_layer(x, x_2, self.layer11)
        x, x_2 = sum_outputs_and_feed_to_layer(x, x_2, self.layer12)
        x, x_2 = sum_outputs_and_feed_to_layer(x, x_2, self.layer13)
        x, x_2 = sum_outputs_and_feed_to_layer(x, x_2, self.layer14)
        x, x_2 = sum_outputs_and_feed_to_layer(x, x_2, self.layer15)
        x, x_2 = sum_outputs_and_feed_to_layer(x, x_2, self.layer16)
        x, x_2 = sum_outputs_and_feed_to_layer(x, x_2, self.layer17)
        x, x_2 = sum_outputs_and_feed_to_layer(x, x_2, self.layer18)
        return x_2
